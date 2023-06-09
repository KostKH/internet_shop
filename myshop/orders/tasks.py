from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """Задача на отправку e-mail после успешного создания заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (f'Dear {order.first_name},\n\n'
               'You have successfully placed an order.'
               f'Your order ID is {order.id}.')
    return send_mail(subject,
                     message,
                     'admin@myshop.com',
                     [order.email])
