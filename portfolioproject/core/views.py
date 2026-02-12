from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import Contact

def home_view(request):
    return render(request, "core/home.html")

def about_view(request):
    return render(request, "core/about.html")

def projects_view(request):
    return render(request, "core/project.html")

# def contact_view(request):
    return render(request, "core/contact.html")




# def contact_view(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         Contact.objects.create(
#             name=name,
#             email=email,
#             message=message
#         )

#         return redirect("contact")

#     return render(request, "core/contact.html")
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and message:
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
            )


        return redirect("contact")

    return render(request, "core/contact.html")



