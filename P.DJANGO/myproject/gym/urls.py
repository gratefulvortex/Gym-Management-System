from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('login.html', views.login_page, name='login_html'),
    path('membership/', views.membership_page, name='membership'), 
    path('take-attendance/', views.take_attendance_page, name='take_attendance'),
    path('employee/', views.employee_page, name='employee'),
    path('logout/', views.logout_view, name='logout'), # Add logout URL patterns
    path('members/', views.members_page, name='members'),
    path('welcome/', views.welcome_page, name='welcome'),
    path('members/', views.members_page, name='members_page'), 
    path('renew-membership/<int:member_id>/', views.renew_membership, name='renew_membership'),  # New URL pattern
]