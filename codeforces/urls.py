from django.contrib import admin
from django.urls import path, include
from homepage import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('homepage.urls')),
    path('stalk/<str:handle>', home_views.stalk, name='stalk'),
]
