from django.urls import path
from . import views

urlpatterns = [
    path('http/', views.http_all),
    path('http/<str:domain>', views.http_filter),
    path('http/tech/<str:tech>', views.http_filter_tech),
    path('http/title/<str:title>', views.http_filter_title),
    path('http/fresh/', views.http_fresh_all),
    path('http/fresh/<str:domain>', views.http_fresh_filter),
    path('http/fresh/tech/<str:tech>', views.http_fresh_filter_tech),
    path('http/fresh/title/<str:title>', views.http_fresh_filter_title),

]