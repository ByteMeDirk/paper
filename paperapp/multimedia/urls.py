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
    path("hide_post/<str:post_type>/<int:post_id>/", views.hide_post, name="hide_post"),
    path(
        "unhide_post/<str:post_type>/<int:post_id>/",
        views.unhide_post,
        name="unhide_post",
    ),
    path("view_post/<str:post_type>/<int:post_id>/", views.view_post, name="view_post"),
    path("search/", views.search, name="search"),
    path(
        "vote/<int:media_id>/<str:media_type>/<str:vote_type>/", views.vote, name="vote"
    ),
    path("view_gallery/<str:media_type>", views.view_gallery, name="view_gallery"),
]
