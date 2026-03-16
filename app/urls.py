from django.urls import path

from .views import (
    analytics_summary,
    data_intake_upload_page,
    finance_transactions,
    landing_page,
    nepal_trust_map_page,
    process_upload,
    secure_access_login_page,
    sovereign_dashboard_page,
    stitch_page,
    trust_analytics_page,
    upload_media,
    verified_finance_page,
)

app_name = 'app'

urlpatterns = [
    path('', landing_page, name='landing_root'),
    path('stitch-ui/<slug:page_slug>/', stitch_page, name='stitch_page'),
    path('landing-page/', landing_page, name='landing_page'),
    path('secure-access-login/', secure_access_login_page, name='secure_access_login'),
    path('sovereign-dashboard/', sovereign_dashboard_page, name='sovereign_dashboard'),
    path('trust-analytics/', trust_analytics_page, name='trust_analytics'),
    path('nepal-trust-map/', nepal_trust_map_page, name='nepal_trust_map'),
    path('verified-finance/', verified_finance_page, name='verified_finance'),
    path('data-intake-upload/', data_intake_upload_page, name='data_intake_upload'),
    path('api/upload/', upload_media, name='upload_media'),
    path('api/upload/<int:upload_id>/process/', process_upload, name='process_upload'),
    path('uploads/<int:upload_id>/process/', process_upload, name='process_upload_action'),
    path('api/analytics/summary/', analytics_summary, name='analytics_summary'),
    path('api/finance/transactions/', finance_transactions, name='finance_transactions'),
]
