from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('application_list/', views.ApplicationListView.as_view(), name='application_list'),
    path('application_create/', views.ApplicationCreateView.as_view(), name='applications_create'),
    path('application_delete/<int:pk>/', views.ApplicationDelete.as_view(), name='application_delete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logged_out/', views.LogoutView.as_view(), name='logged_out'),
    path('profile/filter/', views.ProfileFilter.as_view(), name='profile_filter'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('portal/category_list/', views.category_list, name="category_list"),
    path('portal/category/create/', views.category_create, name="category_create"),
    path('portal/category/delete/<int:pk>/', views.category_delete, name="category_delete"),
    path('application/change/status/done/<int:pk>/', views.ApplicationUpdateStatusDoneView.as_view(),
         name="application_change_status_done"),
    path('application/change/status/inwork/<int:pk>/', views.ApplicationUpdateStatusInWorkView.as_view(),
         name="application_change_status_inwork"),
]