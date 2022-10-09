from django.db import models
from django.db.models import QuerySet, Window, F
from django.db.models.functions import Lag
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.rental.api.pagination import ReservationsPagination
from apps.rental.api.serializers import ReservationListSerializer
from apps.rental.models import Reservation


class ReservationViewSet(ListModelMixin, GenericViewSet):
    # We support only list/retrieve methods so far
    http_method_names = ["get", "options", "head"]
    serializer_class = ReservationListSerializer
    pagination_class = ReservationsPagination

    def get_queryset(self) -> QuerySet:
        qs = Reservation.objects.select_related("rental").annotate(
            previous_reservation_id=Window(
                expression=Lag("id"),
                partition_by=F("rental_id"),
                order_by=("rental_id", "checkin"),
                output_field=models.IntegerField(),
            )
        )
        return qs
