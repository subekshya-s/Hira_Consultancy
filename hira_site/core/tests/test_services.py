import pytest
from core.models import Service
from django.urls import reverse

@pytest.mark.django_db
def test_service_list_page_shows_services(client):
    Service.objects.create(title="Structural Survey",description="x")
    response = client.get(reverse("service_list"))
    assert response.status_code == 200
    assert b"Structural Survey" in response.content

@pytest.mark.django_db
def test_service_detail_page_shows_the_service(client):
    service = Service.objects.create(title= "Structural Survey",description="Shirt text.")
    response = client.get(reverse("service_detail", args=[service.slug]))    
    assert response.status_code == 200
    assert b"Short text." in response.content


@pytest.mark.django_db
def test_unknown_service_returns_404(client):
    response = client.get("/services/does-not-exist/")
    assert response.status_code ==404