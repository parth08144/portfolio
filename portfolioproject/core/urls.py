from django.urls import path
from .views import home_view, about_view, projects_view, contact_view

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("projects/", projects_view, name="projects"),
    path("contact/", contact_view, name="contact"),
]
