from django.urls import path
from . import views

urlpatterns = [
    path('subdomains/', views.subdomain_all),
    path('subdomains/<str:domain>', views.subdomain_filter),
]