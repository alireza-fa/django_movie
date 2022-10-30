from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/verify_account/', views.VerifyAccountView.as_view(), name='verify_account'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forget/', views.ForgetPasswordView.as_view(), name='forget'),
    path('forget/verify/', views.ForgetPasswordVerifyView.as_view(), name='forget_verify'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
