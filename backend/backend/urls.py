from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls"))
]
