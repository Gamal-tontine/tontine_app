from django.urls import path

from .views import CreateTontineView,JoingedTontineView,DetailTontineView,PageLinkTontineView,DeleteTontineView
from .views import UpdateTontineView,demarrer_tontine

app_name = 'tontine'
urlpatterns = [
    path('create-tontine/',CreateTontineView.as_view(),name='create_tontine'),
    path('joindre-tontine/<str:uid>/',JoingedTontineView.as_view(),name='joined_tontine'),
    path('detail-tontine/<str:uid>/',DetailTontineView.as_view(),name='detail_tontine'),
    path('Lien-join-tontine/<str:uid>',PageLinkTontineView.as_view(),name='link_join_tontine'),
    path('delete-tontine/<str:uid>/',DeleteTontineView.as_view(),name='delete_tontine'),
    path('update-tontine/<str:uid>/',UpdateTontineView.as_view(),name='update_tontine'),
    path('damare/<str:uid>',demarrer_tontine,name='demarer'),
]
