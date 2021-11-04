from django.urls import path

from . import util


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("submit", views.submit, name="submit"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("random", views.random, name="random")
]
