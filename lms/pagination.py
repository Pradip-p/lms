from rest_framework import serializers, pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10  # Set the number of items per page

