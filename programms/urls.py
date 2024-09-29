from django.urls import path
from . import views

urlpatterns = [
    path('programms/', views.programm_list),
]