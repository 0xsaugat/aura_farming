from django.urls import path

from .views import home

app_name = 'analyzer'

urlpatterns = [
    path('', home, name='home'),
]
