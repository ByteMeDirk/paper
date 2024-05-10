from django.urls import path

from . import views

urlpatterns = [
    path("report_user/<int:user_id>/", views.report_user, name="report_user"),
    path("report_post/<int:post_id>/<str:post_type>/", views.report_post, name="report_post"),
]
