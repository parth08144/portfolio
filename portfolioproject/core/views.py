from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Project, Contact
from .forms import ProjectForm


# ----------------------------
# Helper: Only Admin Access
# ----------------------------
def is_admin(user):
    return user.is_superuser


# ----------------------------
# Home & About
# ----------------------------
def home_view(request):
    return render(request, "core/home.html")


def about_view(request):
    return render(request, "core/about.html")


# ----------------------------
# Contact View
# ----------------------------
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and message:
            # Save to database
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            # Email to you (admin)
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=f"""
Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )

            # Auto reply to user
            send_mail(
                subject="Thank You for Contacting Me 🚀",
                message=f"""
Hi {name},

Thank you for reaching out.
I have received your message and will get back to you soon.

Regards,
Parth Tripathi
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            messages.success(request, "Message sent successfully!")

        return redirect("contact")

    return render(request, "core/contact.html")


# ----------------------------
# Projects Display
# ----------------------------
def projects_view(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "core/project.html", {"projects": projects})


# ----------------------------
# Signup (Optional - if needed)
# ----------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})


# ----------------------------
# Login / Logout
# ----------------------------
class CustomLoginView(LoginView):
    template_name = "core/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/"


# ----------------------------
# Add Project (ADMIN ONLY)
# ----------------------------
@user_passes_test(is_admin)
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("projects")
    else:
        form = ProjectForm()

    return render(request, "core/add_project.html", {"form": form})


# ----------------------------
# Delete Project (ADMIN ONLY)
# ----------------------------
@user_passes_test(is_admin)
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("projects")

from django.contrib.auth.decorators import login_required

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)   # 🚨 DON'T SAVE YET
            project.user = request.user         # ✅ Assign logged-in user
            project.save()                      # ✅ Now save
            return redirect("projects")
    else:
        form = ProjectForm()

    return render(request, "core/add_project.html", {"form": form})
