from django.contrib import admin

from .models import CarBrand, Engine, CategoryOperations, Operation, Order


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title',]


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'engine_type']
    search_fields = ['title', 'engine_type']


@admin.register(CategoryOperations)
class CategoryOperationsAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['title', 'engine', 'category', 'price']
    list_editable = ['price']
    list_filter = ['title', 'engine']
    search_fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['id',]
    filter_horizontal = ('operation',)
    list_display = ['id',
                    'customer_name',
                    'customer_phone_number',
                    'engine',
                    'total_amount']
    list_editable = ['total_amount',]
    list_filter = ['customer_name',]
    list_max_show_all = 100
    list_select_related = ['engine']
    search_fields = ['id', 'customer_name']
    date_hierarchy = "accept_date"

    @staticmethod
    def sum_operations(data_form):
        cost_operations = 0
        operations = data_form

        for operation in operations:
            cost_operations += operation.price

        return cost_operations

    @staticmethod
    def set_id():
        try:
            last_order = Order.objects.order_by('id').last()
            order_number = last_order.id + 1
        except AttributeError:
            order_number = 1
        return order_number

    def save_model(self, request, obj, form, change):
        obj.total_amount = self.sum_operations(form.cleaned_data['operation'])
        if not change:
            obj.id = self.set_id()
        super().save_model(request, obj, form, change)
