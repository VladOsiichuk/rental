from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import ReservationFactory
from tests.integration.reservations.api.constants import RESERVATIONS_ENDPOINT


def test_paginated_response_returned(api_client: APIClient) -> None:
    expected_response_keys = {"next", "previous", "results"}
    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    assert set(response.json().keys()) == expected_response_keys


def test_reservation_item_fields(api_client: APIClient):
    reservation = ReservationFactory()
    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 1
    actual_reservation_data = data["results"][0]
    expected_reservation_data = {
        "id": reservation.id,
        "previous_reservation_id": None,
        "checkin": str(reservation.checkin),
        "checkout": str(reservation.checkout),
        "rental_name": reservation.rental.name,
    }

    assert expected_reservation_data == actual_reservation_data


def test_reservations_ordering(api_client: APIClient) -> None:
    """
    Reservations should be ordered by rental id and checkin then
    """
    first_reservation = ReservationFactory()
    second_reservation = ReservationFactory(rental=first_reservation.rental)
    # It has another rental
    third_reservation = ReservationFactory()
    fourth_reservation = ReservationFactory(rental=first_reservation.rental)

    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    expected_reservations_ordering = [
        first_reservation.id,
        second_reservation.id,
        fourth_reservation.id,
        third_reservation.id,
    ]
    results = response.json()["results"]
    actual_reservations_ordering = [row["id"] for row in results]
    assert expected_reservations_ordering == actual_reservations_ordering


def test_previous_reservation_link_related_to_previous_rental_reservation(
    api_client: APIClient,
) -> None:
    first_reservation = ReservationFactory()
    ReservationFactory(rental=first_reservation.rental)

    # Generate reservation which is not related to previous reservations rental
    ReservationFactory()

    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 3
    assert data["results"][0]["previous_reservation_id"] is None
    second_reservation_data = data["results"][1]
    assert second_reservation_data["previous_reservation_id"] == first_reservation.id


def test_previous_reservation_link_for_two_rentals(api_client: APIClient) -> None:
    first_rental_reservation = ReservationFactory()
    ReservationFactory(rental=first_rental_reservation.rental)

    second_rental_reservation = ReservationFactory()
    ReservationFactory(rental=second_rental_reservation.rental)
    response = api_client.get(RESERVATIONS_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 4
    assert data["results"][1]["previous_reservation_id"] == first_rental_reservation.id
    assert data["results"][3]["previous_reservation_id"] == second_rental_reservation.id
