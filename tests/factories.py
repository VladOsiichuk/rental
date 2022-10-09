from datetime import timedelta

import factory
import factory.fuzzy
from django.utils import timezone

from apps.rental.models import Rental, Reservation


class RentalFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"rental-{n}")

    class Meta:
        model = Rental


class ReservationFactory(factory.django.DjangoModelFactory):
    rental = factory.SubFactory(RentalFactory)
    checkin = factory.Sequence(lambda n: timezone.now().date() + timedelta(days=n))
    checkout = factory.LazyAttribute(
        lambda reservation: reservation.checkin + timedelta(days=1)
    )

    class Meta:
        model = Reservation
