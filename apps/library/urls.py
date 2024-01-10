from django.urls import path

from apps.library import views

urlpatterns = [
    path('', views.SavedBookListCreateAPIView.as_view(), name='library'),
    path('<int:id>/', views.SavedBookRetrieveUpdateDestroyAPIView.as_view(), name='update_library'),
]
