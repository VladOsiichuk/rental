from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.rental.models import Reservation


class ReservationListSerializer(ModelSerializer):
    rental_name = serializers.CharField(source="rental.name")
    previous_reservation_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reservation
        fields = ("rental_name", "id", "checkin", "checkout", "previous_reservation_id")
        read_only_fields = fields
