import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from core.models import Alliance
from core.views import AllianceCrud


@pytest.mark.django_db
def test_alliance():
    user = User.objects.create_user('test', 'test@test.com', 'testtest')

    url = reverse("crud-alliance")
    data = {
        "q": "bjp",
        "party": "nda"
    }

    alliances = Alliance.objects.filter(q=data['q'])
    assert len(alliances) == 0

    request = APIRequestFactory()
    request.get(url)
    force_authenticate(request, user=user)
    response = AllianceCrud().get(request)
    assert response.status_code == 200

    request = APIRequestFactory()
    setattr(request, "data", {})
    request.post(url)
    force_authenticate(request, user=user)
    response = AllianceCrud().post(request)
    assert response.status_code == 422

    request = APIRequestFactory()
    setattr(request, "data", data)
    request.post(url)
    force_authenticate(request, user=user)
    response = AllianceCrud().post(request)
    assert response.status_code == 200
    alliances = Alliance.objects.filter(q=data['q'])
    assert len(alliances) == 1

    alliance = Alliance.objects.get(q=data['q'])
    assert alliance.get_party_display() == "nda"
    request.patch(url)
    request = APIRequestFactory()
    data['party'] = "upa"
    setattr(request, "data", data)
    force_authenticate(request, user=user)
    response = AllianceCrud().patch(request)
    assert response.status_code == 200
    alliance = Alliance.objects.get(q=data['q'])
    assert alliance.get_party_display() == "upa"

    request = APIRequestFactory()
    setattr(request, "data", data)
    request.delete(url)
    force_authenticate(request, user=user)
    response = AllianceCrud().delete(request)
    assert response.status_code == 200
    alliances = Alliance.objects.filter(q=data['q'])
    assert len(alliances) == 0
