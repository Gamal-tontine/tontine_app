from django.urls import path

from .views import dashboard

app_name = 'admin_tontine'
urlpatterns = [
    path('dashboard/',dashboard, name='dashboard')
]
