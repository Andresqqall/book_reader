from django.urls import path

from apps.auth import views

urlpatterns = [

    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('confirm_registration/', views.ConfirmRegistrationAPIView.as_view(), name='confirm_registration')

]
