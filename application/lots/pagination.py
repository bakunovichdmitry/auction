from rest_framework import pagination


class LotPagination(pagination.PageNumberPagination):
    page_size = 5
