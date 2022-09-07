from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/action/<int:pk>/', views.UserActionView.as_view(), name='user_action'),
    path('users/edit/<int:user_id>/', views.UserEditView.as_view(), name='user_edit'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('contacts/action/<int:pk>/', views.ContactActionView.as_view(), name='contact_action'),
]
