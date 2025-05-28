from django.db.models import Q
from django.db.models.query import QuerySet
from suppliers.models import Supplier

class SupplierFilter:
    def __init__(self, request):
        self.params = request.query_params

    def apply_filters(self, queryset: QuerySet[Supplier]) -> QuerySet[Supplier]:
        # Apply rating filters
        rating_min = self.params.get('rating_min')
        rating_max = self.params.get('rating_max')
        if rating_min:
            queryset = queryset.filter(rating__gte=rating_min)
        if rating_max:
            queryset = queryset.filter(rating__lte=rating_max)

        # Apply search filter
        search = self.params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search)
            )

        # Apply active filter
        is_active = self.params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset 