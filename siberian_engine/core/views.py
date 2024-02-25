from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Engine, Order, Operation


class DashView(View):
    def get(self, request):
        engine = Engine.objects.all()
        orders_accept = Order.objects.filter(status='Принят')
        orders_in_progres = Order.objects.filter(status='В работе')
        orders_complete = Order.objects.filter(status='Готов')
        return render(request, 'core/dashboard.html', {
            'engine': engine,
            'orders_accept': orders_accept,
            'orders_in_progress': orders_in_progres,
            'orders_complete': orders_complete,

        })


class EngineList(ListView):
    model = Engine
    template_name = 'core/engine_list'
    context_object_name = 'engines'


class OperationList(ListView):
    model = Operation
    template_name = 'core/operation_list'
    context_object_name = 'operations'


class OrderList(ListView):
    model = Order
    template_name = 'core/order_list'
    context_object_name = 'orders'


class OrderDetail(DetailView):
    model = Order
