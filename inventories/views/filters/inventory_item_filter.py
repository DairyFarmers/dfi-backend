class InventoryItemFilter:
    def __init__(self, request):
        self.params = request.query_params
        
    def apply_filters(self, queryset):
        # Apply quantity filters
        min_quantity = self.params.get('min_quantity')
        max_quantity = self.params.get('max_quantity')
        if min_quantity:
            queryset = queryset.filter(quantity__gte=min_quantity)
        if max_quantity:
            queryset = queryset.filter(quantity__lte=max_quantity)

        # Apply date filters
        expiry_before = self.params.get('expiry_before')
        expiry_after = self.params.get('expiry_after')
        if expiry_before:
            queryset = queryset.filter(expiry_date__lte=expiry_before)
        if expiry_after:
            queryset = queryset.filter(expiry_date__gte=expiry_after)

        # Apply choice filters
        dairy_type = self.params.get('dairy_type')
        storage_condition = self.params.get('storage_condition')
        if dairy_type:
            queryset = queryset.filter(dairy_type=dairy_type)
        if storage_condition:
            queryset = queryset.filter(storage_condition=storage_condition)

        # Apply supplier filter
        supplier = self.params.get('supplier')
        if supplier:
            queryset = queryset.filter(supplier_id=supplier)

        # Apply active filter
        is_active = self.params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset 