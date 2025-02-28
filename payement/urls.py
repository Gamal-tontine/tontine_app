from django.urls import path

from .views import AcquitementCollectiveView
from .views import AcquitementIndividuelleAdmin
from .views import AcquitementIndividuelleUserView
from .views import HistoriqueView
from .views import PayementCollective
from .views import PayementIndividuelleView
from .views import unblock_user_after_payment

app_name = 'payement'
urlpatterns = [
    path('acquitement/<str:uid_tontine>/<int:id_user>/',
         AcquitementCollectiveView.as_view(), name='acquitement_collective_admin'),
    path('payement-collective/<str:uid>/', PayementCollective.as_view(),
         name='payement_tontine_collective'),
    path('historique/<int:user>/<str:tontine>/',
         HistoriqueView.as_view(), name='historique'),
    path('acquitement-tontine/<str:uid>/', AcquitementIndividuelleAdmin.as_view(),
         name='acquitement_tontine_individuelle_admin'),
    path('acquitement-tontine-user/<str:uid>/', AcquitementIndividuelleUserView.as_view(),
         name='acquitement_tontine_individuelle_user'),
    path('payement-tontine/<str:uid>/', PayementIndividuelleView.as_view(),
         name='payement_tontine_individuelle'),
    path('unlock-user/<str:tontine_uid>/<int:user_id>/',
         unblock_user_after_payment, name="unlock_user")


]
