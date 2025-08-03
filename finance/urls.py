from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
