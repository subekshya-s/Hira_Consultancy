from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import QuoteRequestForm
from .models import Partner, Project, Service, SiteSettings, Stat


def home(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. We received your request and will reply soon.")
            return redirect(f"{reverse('home')}#contact")
    else:
        form = QuoteRequestForm()

    projects = Project.objects.all()
    # Only projects that have coordinates become pins on the map.
    map_points = [
        {"name": p.name, "location": p.location, "lat": p.latitude, "lng": p.longitude}
        for p in projects
        if p.has_coordinates
    ]

    context = {
        "site": SiteSettings.load(),
        "services": Service.objects.all(),
        "featured_projects": projects.filter(featured=True)[:4],
        "stats": Stat.objects.all(),
        "partners": Partner.objects.all(),
        "map_points": map_points,
        "form": form,
    }
    return render(request, "core/home.html", context)
