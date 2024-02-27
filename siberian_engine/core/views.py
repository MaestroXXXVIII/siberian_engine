from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Engine, Order, Operation


class DashView(View):

    def get_context_data(self):
        context = {}
        context['engines'] = Engine.objects.all()
        context['orders_accept'] = Order.objects.filter(status='Принят')
        context['orders_in_progress'] = Order.objects.filter(status='В работе')
        context['orders_complete'] = Order.objects.filter(status='Готов')
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'core/dashboard.html', context)


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
