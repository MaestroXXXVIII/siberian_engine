import json
import weasyprint

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.core.cache import cache
from django.core.serializers import serialize
from django.views.generic import ListView, UpdateView, CreateView
from django.template.loader import render_to_string

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
            cache.set(settings.ENGINE_CACHE_NAME, queryset, 3600 * 8)
        return queryset


class EngineCreate(CreateView):
    model = Engine
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('engine_list')


class EngineUpdate(UpdateView):
    model = Engine
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('engine_list')


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


class OperationCreate(CreateView):
    model = Operation
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('operation_list')


class OperationUpdate(UpdateView):
    model = Operation
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('operation_list')


class OrderList(ListView):
    model = Order

    queryset = (Order.objects.all().select_related('engine', 'engine__brand')
                                   .prefetch_related('operation'))
    template_name = 'core/order/order_list.html'
    context_object_name = 'orders'


class OrderCreate(CreateView):
    model = Order
    fields = '__all__'
    template_name = 'core/order/order_create_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        order = form.instance

        total_amount = calculate_total_amount(form)
        order.total_amount = total_amount
        order.id = Order.objects.count() + 1

        order.save()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'core/order/order_update_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        order = form.instance

        total_amount = calculate_total_amount(form)
        order.total_amount = total_amount

        order.save()

        return super().form_valid(form)


def calculate_total_amount(form):
    operations = form.cleaned_data.get('operation')
    total_amount = sum(operation.price for operation in operations)
    return total_amount


def get_operations_by_engine(request):
    try:
        body = request.body.decode('utf-8')
        data = json.loads(body)
        engine_id = data.get('engine')
        operations = serialize('json', Operation.objects
                                                .filter(engine__id=engine_id))

        return JsonResponse({'operations': operations})

    except Operation.DoesNotExist:

        return JsonResponse({'operations': ''})


def order_pdf(request, pk):
    order = Order.objects.get(id=pk)
    operations = order.operation.all().select_related('engine')
    html = render_to_string('core/order/order_pdf.html', {
                            'order': order,
                            'operations': operations
                            })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html) \
              .write_pdf(response,
                         stylesheets=[weasyprint.CSS(f'{settings.STATIC_DIR}/'
                                                     f'css/order_pdf.css')])
    return response
