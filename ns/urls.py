from django.urls import path
from . import views

urlpatterns = [
    path('lives/', views.live_all),
    path('lives/<str:domain>', views.live_filter),
]