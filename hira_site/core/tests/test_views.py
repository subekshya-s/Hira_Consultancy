import pytest
from django.urls import reverse

from core.models import Project, QuoteRequest, Service


@pytest.mark.django_db
def test_home_page_loads(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"Hira Engineering Consultancy" in response.content


@pytest.mark.django_db
def test_services_from_database_are_shown(client):
    Service.objects.create(title="Structural Design", description="Safe designs.", order=1)
    response = client.get(reverse("home"))
    assert b"Structural Design" in response.content


@pytest.mark.django_db
def test_only_projects_with_coordinates_become_map_pins(client):
    Project.objects.create(name="With pin", latitude=27.67, longitude=85.34)
    Project.objects.create(name="No pin")
    response = client.get(reverse("home"))
    assert len(response.context["map_points"]) == 1


@pytest.mark.django_db
def test_valid_quote_request_is_saved(client):
    data = {"name": "Sita", "email": "sita@example.com", "phone": "", "message": "A 3 storey house."}
    response = client.post(reverse("home"), data)
    assert response.status_code == 302
    assert QuoteRequest.objects.count() == 1


@pytest.mark.django_db
def test_quote_request_without_message_is_rejected(client):
    data = {"name": "Sita", "email": "sita@example.com", "phone": "", "message": ""}
    response = client.post(reverse("home"), data)
    assert response.status_code == 200
    assert QuoteRequest.objects.count() == 0
