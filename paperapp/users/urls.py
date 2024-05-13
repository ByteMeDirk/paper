from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.user_profile, name="profile"),
    path("user/<int:user_id>/", views.view_user, name="view_user"),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
]
