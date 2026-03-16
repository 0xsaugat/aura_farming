from django.http import Http404
from django.shortcuts import render


STITCH_PAGES = {
	'landing-page': {
		'label': 'Landing Page',
		'template': 'stitch_ui/landing_page.html',
	},
	'secure-access-login': {
		'label': 'Secure Access Login',
		'template': 'stitch_ui/secure_access_login.html',
	},
	'sovereign-dashboard': {
		'label': 'Sovereign Dashboard',
		'template': 'stitch_ui/sovereign_dashboard.html',
	},
	'trust-analytics': {
		'label': 'Trust Analytics',
		'template': 'stitch_ui/trust_analytics.html',
	},
	'nepal-trust-map': {
		'label': 'Nepal Trust Map',
		'template': 'stitch_ui/nepal_trust_map.html',
	},
	'verified-finance': {
		'label': 'Verified Finance',
		'template': 'stitch_ui/verified_finance.html',
	},
	'data-intake-upload': {
		'label': 'Data Intake Upload',
		'template': 'stitch_ui/data_intake_upload.html',
	},
}


def home(request):
	return render(
		request,
		'analyzer/home.html',
		{
			'stitch_pages': STITCH_PAGES,
		},
	)


def stitch_page(request, page_slug):
	page = STITCH_PAGES.get(page_slug)
	if not page:
		raise Http404('Page not found')

	return render(
		request,
		page['template'],
		{
			'current_page': page_slug,
			'stitch_pages': STITCH_PAGES,
		},
	)
