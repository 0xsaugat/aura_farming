from django.contrib import admin

from .models import (
	CarbonRecord,
	FinanceTransaction,
	MediaUpload,
	TreeDetection,
	UserProfile,
	VerificationLedger,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'role', 'organization', 'created_at')
	search_fields = ('user__username', 'organization')


@admin.register(MediaUpload)
class MediaUploadAdmin(admin.ModelAdmin):
	list_display = ('id', 'media_type', 'province', 'district', 'status', 'upload_date')
	list_filter = ('media_type', 'status', 'province')


@admin.register(TreeDetection)
class TreeDetectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'media', 'tree_count', 'confidence_score', 'forest_density_score', 'processed_at')


@admin.register(CarbonRecord)
class CarbonRecordAdmin(admin.ModelAdmin):
	list_display = ('id', 'tree_count', 'carbon_tons', 'estimated_value', 'verification_status', 'created_at')


@admin.register(VerificationLedger)
class VerificationLedgerAdmin(admin.ModelAdmin):
	list_display = ('id', 'carbon_record', 'verified', 'timestamp')
	search_fields = ('hash_value',)


@admin.register(FinanceTransaction)
class FinanceTransactionAdmin(admin.ModelAdmin):
	list_display = ('id', 'buyer_company', 'total_value', 'payment_status', 'transaction_date')
	list_filter = ('payment_status',)
