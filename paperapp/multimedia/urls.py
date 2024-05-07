from django.urls import path

from . import views

urlpatterns = [
    path("select_post_type/", views.select_post_type, name="select_post_type"),
    path("create_post/<str:post_type>/", views.create_post, name="create_post"),
    path("edit_post/<str:post_type>/<int:post_id>/", views.edit_post, name="edit_post"),
    path(
        "delete_post/<str:post_type>/<int:post_id>/",
        views.delete_post,
        name="delete_post",
    ),
]
