from django.urls import path
from .views import home_view, about_view, projects_view, contact_view, CustomLoginView, CustomLogoutView, add_project, delete_project
from . import views
from .views import home_view, about_view, projects_view, contact_view, CustomLoginView, CustomLogoutView, add_project, delete_project

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("projects/", projects_view, name="projects"),
    path("contact/", contact_view, name="contact"),
    path("certifications/", views.certifications, name="certifications"),

    # path("super-secret-admin-login-123/", CustomLoginView.as_view(), name="login"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    path("add-project/", views.add_project, name="add_project"),
    path("delete-project/<int:pk>/", views.delete_project, name="delete_project"),
    path("certifications/", views.certifications, name="certifications"),
    path("add-certificate/", views.add_certificate, name="add_certificate"),
    path("delete-certificate/<int:pk>/", views.delete_certificate, name="delete_certificate"),
]
handler404 = 'portfolioproject.views.custom_404'