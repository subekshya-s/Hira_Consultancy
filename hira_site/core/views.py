from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.db.models import Count
from .forms import QuoteRequestForm
from .models import Partner, Project, Service, SiteSettings, Stat,AboutPhoto


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
        "stats": Stat.objects.all(),
        "partners": Partner.objects.all(),
        "map_points": map_points,
        "form": form,
        "about_photos": AboutPhoto.objects.all(),
    }
    return render(request, "core/home.html", context)

def service_list(request):
    context = {"site": SiteSettings.load(), "services": Service.objects.all()}
    return render(request, "core/services.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {"site": SiteSettings.load(), "service": service}
    return render(request, "core/service_detail.html", context)

def work(request):
    services = Service.objects.annotate(project_count=Count("projects"))
    projects = Project.objects.select_related("service")

    active = None
    slug = request.GET.get("service", "")
    if slug:
        active = services.filter(slug=slug).first()
        if active:
            projects = projects.filter(service=active)

    view = "map" if request.GET.get("view") == "map" else "details"

    map_points = [
        {"name": p.name, "location": p.location, "lat": p.latitude, "lng": p.longitude}
        for p in projects
        if p.has_coordinates
    ]

    context = {
        "site": SiteSettings.load(),
        "services": services,
        "projects": projects,
        "active": active,
        "total": Project.objects.count(),
        "view": view,
        "map_points": map_points,
    }
    return render(request, "core/work.html", context)

def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related("service"), pk=pk)

    related = Project.objects.exclude(pk=project.pk)
    if project.service:
        related = related.filter(service=project.service)
    related = related[:3]

    map_points = []
    if project.has_coordinates:
        map_points = [{
            "name": project.name,
            "location": project.location,
            "lat": project.latitude,
            "lng": project.longitude,
        }]

    context = {
        "site": SiteSettings.load(),
        "project": project,
        "related": related,
        "map_points": map_points,
    }
    return render(request, "core/project_detail.html", context)