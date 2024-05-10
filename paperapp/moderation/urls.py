from django.urls import path

from . import views

urlpatterns = [
    path("report_user/<int:user_id>/", views.report_user, name="report_user"),
    path(
        "report_post/<int:post_id>/<str:post_type>/",
        views.report_post,
        name="report_post",
    ),
    path("moderator_dashboard/", views.moderator_dashboard, name="moderator_dashboard"),
    path(
        "resolve_user_report/<int:report_id>/",
        views.resolve_user_report,
        name="resolve_user_report",
    ),
    path(
        "resolve_post_report/<int:report_id>/",
        views.resolve_post_report,
        name="resolve_post_report",
    ),
    path(
        "reopen_report/<int:report_id>/<str:report_type>/",
        views.reopen_report,
        name="reopen_report",
    ),
]
