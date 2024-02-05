from django.contrib import admin

from .models import Category, Operation, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'user', 'price']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['code',]
    filter_horizontal = ('operation',)
    list_display = ['code',
                    'customer_name',
                    'customer_phone_number',
                    'engine_title',
                    'total_amount']
