from django.urls import path
from .views import CreateUserView, LoginView, ActivationAccountView,AccountFindForPasswordView, NewPasswordView
from .views import profil,LogOutView

app_name = 'account'
urlpatterns = [
    path('singin/',LoginView.as_view(),name='singin'),
    path('singup/',CreateUserView.as_view(), name='singup'),
    path('activation-account/<str:uid>/<str:token>/',ActivationAccountView.as_view(),name='activation_account'),
    path('account-find/',AccountFindForPasswordView.as_view(),name='account-find'),
    path('new-password/<str:uid>/<str:token>/',NewPasswordView.as_view(), name='new_password'),
    path('profile/',profil,name='profile'),
    path('logouit-user/',LogOutView.as_view(), name='logout'),
    
]
