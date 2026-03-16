import hashlib
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
	ADMIN = 'admin', 'Admin'
	RESEARCHER = 'researcher', 'Researcher'
	UPLOADER = 'uploader', 'Uploader'
	CORPORATE_BUYER = 'corporate_buyer', 'Corporate Buyer'


class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=32, choices=UserRole.choices, default=UserRole.UPLOADER)
	organization = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username} ({self.role})'


class MediaType(models.TextChoices):
	VIDEO = 'video', 'Video'
	PHOTO = 'photo', 'Photo'


class UploadStatus(models.TextChoices):
	UPLOADED = 'uploaded', 'Uploaded'
	PROCESSING = 'processing', 'Processing'
	PROCESSED = 'processed', 'Processed'
	FAILED = 'failed', 'Failed'


class MediaUpload(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	file = models.FileField(upload_to='uploads/%Y/%m/%d/')
	media_type = models.CharField(max_length=16, choices=MediaType.choices)
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	province = models.CharField(max_length=100)
	district = models.CharField(max_length=100)
	status = models.CharField(max_length=16, choices=UploadStatus.choices, default=UploadStatus.UPLOADED)
	upload_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Upload #{self.pk} - {self.media_type}'


class TreeDetection(models.Model):
	media = models.OneToOneField(MediaUpload, on_delete=models.CASCADE, related_name='detection')
	tree_count = models.PositiveIntegerField(default=0)
	species_detected = models.JSONField(default=list, blank=True)
	confidence_score = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))
	forest_density_score = models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('0.000'))
	processed_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'Detection #{self.pk} - {self.tree_count} trees'


class CarbonRecord(models.Model):
	detection = models.OneToOneField(TreeDetection, on_delete=models.CASCADE, related_name='carbon_record')
	tree_count = models.PositiveIntegerField()
	carbon_tons = models.DecimalField(max_digits=10, decimal_places=3)
	price_per_ton = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('30.00'))
	estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
	verification_status = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	@classmethod
	def from_detection(cls, detection, carbon_per_tree_kg=Decimal('22.0'), price_per_ton=Decimal('30.00')):
		carbon_tons = (Decimal(detection.tree_count) * Decimal(carbon_per_tree_kg)) / Decimal('1000')
		estimated_value = carbon_tons * Decimal(price_per_ton)
		return cls.objects.create(
			detection=detection,
			tree_count=detection.tree_count,
			carbon_tons=carbon_tons.quantize(Decimal('0.001')),
			price_per_ton=price_per_ton,
			estimated_value=estimated_value.quantize(Decimal('0.01')),
		)

	def __str__(self):
		return f'CarbonRecord #{self.pk} - {self.carbon_tons} tons'


class VerificationLedger(models.Model):
	carbon_record = models.OneToOneField(CarbonRecord, on_delete=models.CASCADE, related_name='ledger')
	hash_value = models.CharField(max_length=64, unique=True)
	timestamp = models.DateTimeField(default=timezone.now)
	verified = models.BooleanField(default=True)

	@staticmethod
	def build_hash(carbon_record):
		payload = (
			f'{carbon_record.tree_count}|'
			f'{carbon_record.detection.media.latitude}|'
			f'{carbon_record.detection.media.longitude}|'
			f'{carbon_record.carbon_tons}|'
			f'{carbon_record.created_at.isoformat()}'
		)
		return hashlib.sha256(payload.encode('utf-8')).hexdigest()

	@classmethod
	def create_for_record(cls, carbon_record):
		return cls.objects.create(
			carbon_record=carbon_record,
			hash_value=cls.build_hash(carbon_record),
			verified=True,
		)

	def __str__(self):
		return f'Ledger #{self.pk} - {self.hash_value[:10]}...'


class PaymentStatus(models.TextChoices):
	PENDING = 'pending', 'Pending'
	COMPLETED = 'completed', 'Completed'
	FAILED = 'failed', 'Failed'


class FinanceTransaction(models.Model):
	carbon_record = models.ForeignKey(CarbonRecord, on_delete=models.CASCADE, related_name='transactions')
	buyer_company = models.CharField(max_length=255)
	price_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
	total_value = models.DecimalField(max_digits=12, decimal_places=2)
	payment_status = models.CharField(max_length=16, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
	transaction_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'Transaction #{self.pk} - {self.buyer_company}'
