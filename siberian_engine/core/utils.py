import weasyprint

from django.conf import settings
from django.template.loader import render_to_string


def generate_pdf(order, target):
    operations = order.operation.all().select_related('engine')
    html = render_to_string('core/order/order_pdf.html', {
                            'order': order,
                            'operations': operations
                            })
    stylesheets = [weasyprint.CSS(f'{settings.STATIC_DIR}/css/order_pdf.css')]
    weasyprint.HTML(string=html).write_pdf(target, stylesheets=stylesheets)
