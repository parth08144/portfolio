from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Certificate, Project, Contact
from .forms import ProjectForm



def is_admin(user):
    return user.is_superuser



def home_view(request):
    return render(request, "core/home.html")


def about_view(request):
    return render(request, "core/about.html")



from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        
        print("Received:", name, email, phone, message)

        
        if not name or not email or not message:
            messages.error(request, "Please fill all required fields.")
            return redirect("contact")

        try:
            
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            
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
                fail_silently=True,  
            )

            
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
                fail_silently=True,
            )

            messages.success(request, "Message sent successfully!")

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, "Something went wrong. Please try again.")

        return redirect("contact")

    return render(request, "core/contact.html")



def projects_view(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "core/project.html", {"projects": projects})



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



class CustomLoginView(LoginView):
    template_name = "core/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/"



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
            project = form.save(commit=False)   
            project.user = request.user         
            project.save()                      
            return redirect("projects")
    else:
        form = ProjectForm()

    return render(request, "core/add_project.html", {"form": form})



def custom_404(request, exception):
    return render(request, '404error.html', status=404)

def certifications(request):
    return render(request, 'core/certificate.html')




@login_required
def add_certificate(request):
    if request.method == "POST":
        title = request.POST.get('title')
        issuer = request.POST.get('issuer')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        print(title, issuer, image, file)  # 🔥 debug

        Certificate.objects.create(
            title=title,
            issuer=issuer,
            image=image,
            file=file
        )

        return redirect('certifications')

    return render(request, 'core/add_certificate.html')

from django.contrib.auth.decorators import login_required

@login_required
def delete_certificate(request, pk):
    cert = Certificate.objects.get(id=pk)
    cert.delete()
    return redirect('certifications')

@login_required
def add_certificate(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)
        print("FILES:", request.FILES)

        title = request.POST.get('title')
        issuer = request.POST.get('issuer')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        print("VALUES:", title, issuer, image, file)

        if not title or not issuer or not image or not file:
            print("❌ Missing data")
            return redirect('add_certificate')

        Certificate.objects.create(
            title=title,
            issuer=issuer,
            image=image,
            file=file
        )

        print("✅ SAVED SUCCESSFULLY")

        return redirect('certifications')

    return render(request, 'core/add_certificate.html')