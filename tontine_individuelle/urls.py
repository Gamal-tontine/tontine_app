from django.urls import path

from .views import DetailTontineIndividuelleView

urlpatterns = [
    path('detail-tontine-idividelle/', DetailTontineIndividuelleView.as_view(),name='datail_tontine_individuelle'),
    
]
