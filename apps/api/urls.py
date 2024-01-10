from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    path('users/', include('apps.users.urls')),
    path('books/', include('apps.books.urls')),
    path('library/', include('apps.library.urls')),
    path('analytics/', include('apps.analytics.urls')),
]
