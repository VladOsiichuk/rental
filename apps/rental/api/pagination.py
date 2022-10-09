from rest_framework.pagination import CursorPagination


class ReservationsPagination(CursorPagination):
    ordering = ("rental_id", "checkin")
