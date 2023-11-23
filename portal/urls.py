from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('application_list/', views.ApplicationListView.as_view(), name='applications_list'),
    path('application_create/', views.ApplicationCreateView.as_view(), name='applications_create'),
    path('applications_delete/<int:pk>/', views.application_delete, name='applications_delete'),
    path('applications_delete_confirm/<int:pk>/', views.application_delete_confirm, name='applications_delete_confirm'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logged_out/', views.LogoutView.as_view(), name='logged_out'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('categories/', views.categories, name="categories"),
    path('category/create/', views.category_create, name="category_create"),
    path('category/delete/<int:pk>/', views.category_delete, name="category_delete"),
    path('application/delete/<int:pk>/', views.application_delete, name="application_delete"),
    path('application/delete/confirm/<int:pk>/', views.application_delete_confirm, name="application_delete_confirm"),
]