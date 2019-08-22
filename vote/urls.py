from django.contrib import admin
from django.urls import path

from vote import views

urlpatterns = [
    path('', views.show_subjects),
    path('teachers/', views.show_teachers),
    path('praise/', views.praise_or_criticize),
    path('criticize/', views.praise_or_criticize),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('captcha/', views.get_captcha),
    path('login/', views.login),
    path('logout/', views.logout),
]
