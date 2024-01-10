from django.urls import path

from apps.books import views

urlpatterns = [
    path('', views.BookListAPIView.as_view(), name='books_list')
]
