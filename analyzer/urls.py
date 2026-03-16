from django.urls import path

from .views import home, stitch_page

app_name = 'analyzer'

urlpatterns = [
    path('', home, name='home'),
    path('stitch-ui/<slug:page_slug>/', stitch_page, name='stitch_page'),
    path('landing-page/', stitch_page, {'page_slug': 'landing-page'}, name='landing_page'),
    path('secure-access-login/', stitch_page, {'page_slug': 'secure-access-login'}, name='secure_access_login'),
    path('sovereign-dashboard/', stitch_page, {'page_slug': 'sovereign-dashboard'}, name='sovereign_dashboard'),
    path('trust-analytics/', stitch_page, {'page_slug': 'trust-analytics'}, name='trust_analytics'),
    path('nepal-trust-map/', stitch_page, {'page_slug': 'nepal-trust-map'}, name='nepal_trust_map'),
    path('verified-finance/', stitch_page, {'page_slug': 'verified-finance'}, name='verified_finance'),
    path('data-intake-upload/', stitch_page, {'page_slug': 'data-intake-upload'}, name='data_intake_upload'),
]
