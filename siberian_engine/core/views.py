from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page

from .models import Engine, Order, Operation


class DashView(View):

    def get(self, request):
        engines = Engine.objects.all()
        orders = Order.objects.all()
        orders_accept = 0
        orders_in_progress = 0
        orders_complete = 0

        for order in orders:

            if order.status == 'Принят':
                orders_accept += 1
                continue

            if order.status == 'В работе':
                orders_in_progress += 1
                continue

            if order.status == 'Готов':
                orders_complete += 1
                continue

        return render(request,
                      'core/dashboard.html',
                      {
                          'engines': engines,
                          'orders_accept': orders_accept,
                          'orders_in_progress': orders_in_progress,
                          'orders_complete': orders_complete
                      })


class EngineList(ListView):
    model = Engine
    template_name = 'core/engine_list'
    context_object_name = 'engines'

    def get_queryset(self):
        engine_cache = cache.get(settings.ENGINE_CACHE_NAME)
        if engine_cache:
            queryset = engine_cache
        else:
            queryset = Engine.objects.all().select_related('brand')
            cache.set(settings.ENGINE_CACHE_NAME, self.queryset, 3600 * 8)
        return queryset


class OperationList(ListView):
    model = Operation
    template_name = 'core/operation_list'
    context_object_name = 'operations'

    def get_queryset(self):
        operation_cache = cache.get(settings.OPERATION_CACHE_NAME)

        if operation_cache:
            queryset = operation_cache
        else:
            queryset = Operation.objects.all().select_related(
                'category',
                'engine',
                'engine__brand'
            )
            cache.set(settings.OPERATION_CACHE_NAME, queryset, 3600 * 8)

        return queryset


class OrderList(ListView):
    model = Order
    queryset = (Order.objects.all().select_related('engine', 'engine__brand')
                                   .prefetch_related('operation'))
    template_name = 'core/order_list'
    context_object_name = 'orders'


class OrderDetail(DetailView):
    model = Order
