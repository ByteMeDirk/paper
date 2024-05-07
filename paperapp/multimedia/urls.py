from django.urls import path

from . import views

urlpatterns = [
    path("select_post_type/", views.select_post_type, name="select_post_type"),
    path("create_post/<str:post_type>/", views.create_post, name="create_post"),
]
