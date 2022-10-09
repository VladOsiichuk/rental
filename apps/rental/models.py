from django.db import models


class Rental(models.Model):
    name = models.CharField(max_length=64)


class Reservation(models.Model):
    rental = models.ForeignKey(
        Rental, on_delete=models.CASCADE, related_name="reservations"
    )
    checkin = models.DateField()
    checkout = models.DateField()

    class Meta:
        indexes = [models.Index(["rental", "checkin"], name="rental_checkin_idx")]
