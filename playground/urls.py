from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_html, name="home"),
    path('info_home', views.base_info_html, name="info_home"),
    path('about', views.about_html, name="about"),
    path('about_home', views.base_about_html, name="about_home"),
    path('info', views.info_html, name="info"),
    path('add_info', views.add_info, name="add_info"),
    path('delete_info/<info_id>', views.delete_info, name="delete_info")


]