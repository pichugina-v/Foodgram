from rest_framework import pagination


class RecipePagination(pagination.PageNumberPagination):
    page_saze_query_params = 'limit'
