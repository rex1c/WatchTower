from django.urls import path
from . import views

urlpatterns = [
    path('lives/', views.live_all),
    path('lives/<str:domain>', views.live_filter),
    path('lives/fresh/', views.live_fresh_all),
    path('lives/fresh/<str:domain>', views.live_fresh_filter),
    path('lives/provider/<str:provider>', views.live_provider_filter),
]