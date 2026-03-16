from decimal import Decimal
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.utils import timezone

try:
    from huggingface_hub import InferenceClient
except ImportError:  # pragma: no cover - optional dependency in local/dev setups
    InferenceClient = None

from .models import (
    CarbonRecord,
    FinanceTransaction,
    PaymentStatus,
    MediaType,
    TreeDetection,
    UploadStatus,
    VerificationLedger,
)


DEFAULT_SPECIES = ['pine', 'oak', 'rhododendron']
CARBON_PER_TREE_KG = Decimal('22.0')
DEFAULT_PRICE_PER_TON = Decimal('30.00')
HF_MODEL_ID = getattr(settings, 'TREE_DETECTOR_MODEL_ID', 'weecology/deepforest-tree')
HF_SCORE_THRESHOLD = getattr(settings, 'TREE_DETECTOR_SCORE_THRESHOLD', 0.35)
HF_API_TOKEN = getattr(settings, 'HUGGINGFACE_API_TOKEN', None)

_HF_CLIENT = None


def _simulate_detection(upload):
    simulated_tree_count = 30 + (upload.id % 70)
    return {
        'tree_count': simulated_tree_count,
        'species_detected': DEFAULT_SPECIES,
        'confidence_score': Decimal('0.890'),
        'forest_density_score': Decimal('0.820'),
    }


def _get_hf_client():
    global _HF_CLIENT
    if _HF_CLIENT is not None:
        return _HF_CLIENT

    if InferenceClient is None:
        return None

    _HF_CLIENT = InferenceClient(token=HF_API_TOKEN)
    return _HF_CLIENT


def _run_hf_detection(upload):
    if upload.media_type != MediaType.PHOTO:
        raise ValueError('Model inference currently supports photo uploads only.')

    client = _get_hf_client()
    with open(upload.file.path, 'rb') as img_file:
        image_bytes = img_file.read()

    predictions = None
    if client is not None:
        try:
            predictions = client.object_detection(image=image_bytes, model=HF_MODEL_ID)
        except Exception:
            predictions = None

    if predictions is None:
        # Fallback to direct Inference API call for models that don't advertise provider mapping.
        endpoint = f'https://api-inference.huggingface.co/models/{HF_MODEL_ID}'
        headers = {'Content-Type': 'application/octet-stream'}
        if HF_API_TOKEN:
            headers['Authorization'] = f'Bearer {HF_API_TOKEN}'

        request = Request(endpoint, data=image_bytes, headers=headers, method='POST')
        try:
            with urlopen(request, timeout=60) as response:
                raw = response.read().decode('utf-8')
                predictions = json.loads(raw)
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f'HF inference request failed: {exc}') from exc

    if isinstance(predictions, dict) and predictions.get('error'):
        raise RuntimeError(predictions['error'])

    def _get_score(pred):
        if isinstance(pred, dict):
            return float(pred.get('score', 0.0))
        return float(getattr(pred, 'score', 0.0))

    def _get_label(pred):
        if isinstance(pred, dict):
            return str(pred.get('label', 'tree')).lower()
        return str(getattr(pred, 'label', 'tree')).lower()

    filtered = [pred for pred in predictions if _get_score(pred) >= float(HF_SCORE_THRESHOLD)]

    tree_count = len(filtered)
    if tree_count == 0:
        return {
            'tree_count': 0,
            'species_detected': ['tree'],
            'confidence_score': Decimal('0.000'),
            'forest_density_score': Decimal('0.000'),
        }

    unique_labels = sorted({_get_label(pred) for pred in filtered})
    average_score = sum(_get_score(pred) for pred in filtered) / tree_count
    density_score = min(1.0, tree_count / 100.0)

    return {
        'tree_count': tree_count,
        'species_detected': unique_labels or ['tree'],
        'confidence_score': Decimal(str(round(average_score, 3))),
        'forest_density_score': Decimal(str(round(density_score, 3))),
    }


def process_media_upload(upload):
    upload.status = UploadStatus.PROCESSING
    upload.save(update_fields=['status'])

    try:
        detection_data = _run_hf_detection(upload)
    except Exception:
        # Keep the pipeline resilient in dev/offline mode.
        detection_data = _simulate_detection(upload)

    detection, _ = TreeDetection.objects.update_or_create(
        media=upload,
        defaults={
            'tree_count': detection_data['tree_count'],
            'species_detected': detection_data['species_detected'],
            'confidence_score': detection_data['confidence_score'],
            'forest_density_score': detection_data['forest_density_score'],
            'processed_at': timezone.now(),
        },
    )

    carbon_tons = (Decimal(detection.tree_count) * CARBON_PER_TREE_KG / Decimal('1000')).quantize(Decimal('0.001'))
    estimated_value = (carbon_tons * DEFAULT_PRICE_PER_TON).quantize(Decimal('0.01'))

    carbon_record, _ = CarbonRecord.objects.update_or_create(
        detection=detection,
        defaults={
            'tree_count': detection.tree_count,
            'carbon_tons': carbon_tons,
            'price_per_ton': DEFAULT_PRICE_PER_TON,
            'estimated_value': estimated_value,
            'verification_status': True,
        },
    )

    ledger_hash = VerificationLedger.build_hash(carbon_record)
    ledger, _ = VerificationLedger.objects.update_or_create(
        carbon_record=carbon_record,
        defaults={'hash_value': ledger_hash, 'verified': True},
    )

    transaction, _ = FinanceTransaction.objects.get_or_create(
        carbon_record=carbon_record,
        buyer_company='Demo Corporate Buyer',
        defaults={
            'price_per_ton': carbon_record.price_per_ton,
            'total_value': carbon_record.estimated_value,
            'payment_status': PaymentStatus.PENDING,
        },
    )

    upload.status = UploadStatus.PROCESSED
    upload.save(update_fields=['status'])

    return {
        'upload': upload,
        'detection': detection,
        'carbon_record': carbon_record,
        'ledger': ledger,
        'transaction': transaction,
    }
