from django.urls import path
from .views import AcquitementView


app_name = 'payement'
urlpatterns = [
    path('acquitement/<str:uid_tontine>/<int:id_user>/',AcquitementView.as_view(),name='acquitement'),

]
