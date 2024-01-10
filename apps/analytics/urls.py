from django.urls import path

from apps.analytics import views

urlpatterns = [
    path('self/', views.UserAnalyticRetrieveAPIView.as_view(), name='self_analytic')
]
