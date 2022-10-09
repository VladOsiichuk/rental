import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.integration.reservations.api.constants import RESERVATIONS_ENDPOINT


@pytest.mark.parametrize(
    "method,expected_status_code",
    (
        ("GET", status.HTTP_200_OK),
        ("HEAD", status.HTTP_200_OK),
        ("OPTIONS", status.HTTP_200_OK),
        ("POST", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("DELETE", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("PUT", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("PATCH", status.HTTP_405_METHOD_NOT_ALLOWED),
    ),
)
def test_reservations_endpoint_allowed_methods(
    api_client: APIClient, method: str, expected_status_code: int
) -> None:
    response = api_client.request(
        REQUEST_METHOD=method, PATH_INFO=RESERVATIONS_ENDPOINT
    )
    assert response.status_code == expected_status_code


def test_reservations_list_anonymous_user_has_access(api_client: APIClient) -> None:
    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code not in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )
