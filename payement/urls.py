from django.urls import path
from .views import AcquitementView,HistoriqueView


app_name = 'payement'
urlpatterns = [
    path('acquitement/<str:uid_tontine>/<int:id_user>/',AcquitementView.as_view(),name='acquitement'),
    path('historique/<int:user_pk>/<str:tontine_uid>',HistoriqueView.as_view(),name='historique'),
    
]
