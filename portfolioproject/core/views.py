from django.shortcuts import render, redirect

from .models import Contact

def home_view(request):
    return render(request, "core/home.html")

def about_view(request):
    return render(request, "core/about.html")

def projects_view(request):
    return render(request, "core/project.html")

# def contact_view(request):
    return render(request, "core/contact.html")




def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        return redirect("contact")

    return render(request, "core/contact.html")


