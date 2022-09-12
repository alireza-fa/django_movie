from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/action/<int:pk>/', views.UserActionView.as_view(), name='user_action'),
    path('users_deleted/', views.UserDeletedListView.as_view(), name='users_deleted'),
    path('users_deleted/action/<int:pk>/', views.UserDeleteActionView.as_view(), name='user_deleted_action'),
    path('users/edit/<int:pk>/', views.UserEditView.as_view(), name='user_edit'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('contacts/action/<int:pk>/', views.ContactActionView.as_view(), name='contact_action'),
]
