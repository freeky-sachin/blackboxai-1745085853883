from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('agencies/', views.agency_list, name='agency_list'),
    path('agencies/register/', views.agency_register, name='agency_register'),
    path('agencies/<int:pk>/', views.agency_detail, name='agency_detail'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/add/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/edit/', views.resource_update, name='resource_update'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),
    path('alerts/', views.emergency_alerts, name='emergency_alerts'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('map/', views.map_view, name='map_view'),
    path('disasters/<str:disaster_type>/', views.disaster_info, name='disaster_info'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
