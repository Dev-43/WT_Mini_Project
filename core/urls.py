from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('roles/', views.role_list_view, name='role_list'),
    path('roles/<int:role_id>/', views.role_detail_view, name='role_detail'),
    path('roles/<int:role_id>/select/', views.role_select_view, name='role_select'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('result/', views.result_view, name='result'),
    path('tracker/', views.tracker_view, name='tracker'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('export/xml/', views.export_xml_view, name='export_xml'),
    path('api/skills/', views.api_skills_view, name='api_skills'),
    path('api/result/', views.api_result_view, name='api_result'),
]
