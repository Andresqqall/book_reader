from django.urls import path

from apps.users import views

urlpatterns = [
    path('self/', views.UserSelfAPIView.as_view(), name='self_user')
]
