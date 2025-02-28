from django.urls import path

from .views import DashboardView

app_name = 'admin_tontine'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
