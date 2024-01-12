from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("save_content/", views.save_content, name="save_content"),
    path("edit_content/", views.edit_content, name="edit_content"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random_page/", views.random_page, name="random_page"),
]
