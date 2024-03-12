from io import BytesIO
from celery import shared_task

from django.core.mail import EmailMessage

from .utils import generate_pdf
from .models import Order


@shared_task
def order_completed(order_id):
    order = Order.objects.get(id=order_id)

    subject = f'Заказ № {order.id} готов'
    message = f'Здравствуйте, {order.customer_name}!\nВаш {subject}. ' \
              f'Модель двигателя {order.engine}.\nСумма {order.total_amount}'

    email = EmailMessage(subject, message,
                         'urmanov.pro@gmail.com',
                         ['urmanov.2000@mail.ru']
                         )

    out = BytesIO()
    generate_pdf(order, out)

    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')

    email.send()
