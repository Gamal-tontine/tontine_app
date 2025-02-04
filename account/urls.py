from django.urls import path
from .views import CreateUserView, LoginView, ActivationAccoutnView,AccountFindForPasswordView, NewPasswordView

app_name = 'account'
urlpatterns = [
    path('singin/',LoginView.as_view(),name='singin'),
    path('singup/',CreateUserView.as_view(), name='singup'),
    path('activation-account/<str:uid>/<str:token>/',ActivationAccoutnView.as_view,name='activation_account'),
    path('account-find/',AccountFindForPasswordView.as_view(),name='account-find'),
    path('new-password/<str:uid>/<str:token>/',NewPasswordView.as_view(), name='new_password'),
]
