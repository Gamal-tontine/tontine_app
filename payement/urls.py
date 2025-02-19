from django.urls import path
from .views import HistoriqueView, AcquitementIndividuelleAdmin,PayementIndividuelleView,AcquitementIndividuelleUserView,AcquitementCollectiveView
from .views import AcquitementIndividuelleUserView

app_name = 'payement'
urlpatterns = [
    path('acquitement/<str:uid_tontine>/<int:id_user>/',AcquitementCollectiveView.as_view(),name='acquitement_collective_admin'),
    path('historique/<int:user_pk>/<str:tontine_uid>',HistoriqueView.as_view(),name='historique'),
    path('acquitement-tontine/<str:uid>/',AcquitementIndividuelleAdmin.as_view(),name='acquitement_tontine_individuelle_admin'),
    path('acquitement-tontine-user/<str:uid>/',AcquitementIndividuelleUserView.as_view(),name='acquitement_tontine_individuelle_user'),
    path('payement-tontine/<str:uid>/',PayementIndividuelleView.as_view(),name= 'payement_tontine_individuelle'),

    
]
