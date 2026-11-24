from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("our-work/", views.work, name="work"),
    path("our-work/project/<int:pk>/", views.project_detail, name="project_detail"),
    
]
