from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.mom_login, name='login'),
    path('logout/', views.mom_logout, name='logout'),
    path('add-member/', views.add_member, name='add_member'),
    path('view-members/', views.view_members, name='view_members'),
    path('view-members/<str:plan>/', views.view_members, name='view_members_by_plan'),
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('monthly-tracker/', views.monthly_tracker, name='monthly_tracker'),
    path('mark-paid/<int:history_id>/', views.mark_paid, name='mark_paid'),
    path('mark-unpaid/<int:history_id>/', views.mark_unpaid, name='mark_unpaid'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('plan/<int:amount>/', views.plan_table, name='plan_table'),
]
