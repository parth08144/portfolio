from django.urls import path
from .views import home_view, about_view, projects_view, contact_view
from . import views

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("projects/", projects_view, name="projects"),
    path("contact/", contact_view, name="contact"),

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    path("add-project/", views.add_project, name="add_project"),
    path("delete-project/<int:pk>/", views.delete_project, name="delete_project"),
]
