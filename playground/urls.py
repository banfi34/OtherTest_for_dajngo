from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_html, name="home"),
    path('info_home', views.home_info_html, name="info_home"),
    path('contact', views.contact_html, name="contact"),
    path('contact_home', views.home_contact_html, name="contact_home"),
    path('about', views.about_html, name="about"),
    path('about_home', views.home_about_html, name="about_home"),
    path('info', views.info_html, name="info"),
    path('add_info', views.add_info, name="add_info"),
    path('search', views.search, name="search"),
    path('save-review/<int:pid>', views.save_review, name='save-review'),
    path('info_review/<int:id>', views.info_review, name='info_review'),
    path('delete_info/<info_id>', views.delete_info, name="delete_info"),
    path('delete_review/<review_id>', views.delete_review, name="delete_review")

]
