from django.urls import path
from . import views


app_name = 'panel'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/change_user_status/<int:user_id>/', views.ChangeUserStatusView.as_view(), name='change_user_status'),
    path('users/delete/<int:user_id>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/edit/<int:user_id>/', views.UserEditView.as_view(), name='user_edit'),
]
