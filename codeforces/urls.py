from django.contrib import admin
from django.urls import path, include
from homepage import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('homepage.urls')),
    path('stalk/<str:handle>', home_views.stalk, name='stalk'),
    path('submission_statistics/<str:handle>', home_views.submission_statistics, name='submission-statistics'),
    path('contest_statistics/<str:handle>', home_views.contest_statistics, name='contest-statistics')
]
