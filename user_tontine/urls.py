from django.urls import path

from .views import TontineView, TontineCollectiveView, TontineIndividuelleView

app_name = 'user_tontine'

urlpatterns = [
    path('user-dashboard/',TontineView.as_view(),name='user_dashboard'),
    path('tontine-collective/<str:uid>/',TontineCollectiveView.as_view(),name='tontine_collective'),
    path('tontine-individuelle/<str:uid>/',TontineIndividuelleView.as_view(),name='tontine_individuelle'),
]
