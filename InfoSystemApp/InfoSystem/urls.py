from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up', views.signup, name='sign-up'),
    path('auth', views.login, name='auth'),
    path('profile', views.profile, name='profile'),
    path('', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile/add-group', views.add_group, name='add-group'),
    path('profile/groups', views.groups, name='groups'),
    path('profile/groups/<device_group_id>', views.show_group, name='show-group'),
    path('profile/groups/<device_group_id>/edit-group', views.edit_group, name='edit-group'),
    path('profile/groups/<device_group_id>/delete-group', views.delete_group, name='delete-group'),
    path('profile/groups/<device_group_id>/devices/<device_id>', views.show_device, name='show-device'),
    path('profile/groups/<device_group_id>/add-device', views.add_device, name='add-device'),
    path('profile/groups/<device_group_id>/devices/<device_id>/edit-device', views.edit_device, name='edit-device'),
    path('profile/groups/<device_group_id>/devices/<device_id>/delete-device', views.delete_device, name='delete-device'),
    path('profile/groups/<device_group_id>/devices/<device_id>/show-device-token', views.show_device_token, name='show-device-token'),
]