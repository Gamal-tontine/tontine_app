from django.urls import path
from .views import index,about,team,contact,services

app_name = 'blog'
urlpatterns = [
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('team',team,name='team'),
    path('contact',contact,name='contact'),
    path('services',services,name='services'),
]
