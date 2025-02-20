from django.urls import path

from .views import DetailTontineIndividuelleView, CreateTontineIndividuelleView,UpdateTontineView
from .views import delete_tontine_individuelle,CategoryTontineIndividuelle

app_name = 'tontine_individuelle'
urlpatterns = [
    path('detail-tontine-idividelle/<str:uid>/', DetailTontineIndividuelleView.as_view(),name='datail_tontine_individuelle'),
    path('create-tontine-idividelle/', CreateTontineIndividuelleView.as_view(),name='create_tontine_individuelle'),
    path('update-tontine-individuelle/<str:uid>/',UpdateTontineView.as_view(),name= 'update_tontine_individuelle'),
    path('delete-tontine/<str:uid>/',delete_tontine_individuelle,name='delete_tontine_individuelle'),
    path('category-tontine-individuelle/',CategoryTontineIndividuelle.as_view(),name='category_tontine_individuelle')
]
