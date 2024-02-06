from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField('Название', max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Operation(models.Model):
    """Технологическая операция"""
    title = models.CharField('Название', max_length=125)
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE)
    price = models.PositiveIntegerField('Цена')
    user = models.ForeignKey(User,
                             verbose_name='Мастер',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['slug']
        verbose_name = 'операция'
        verbose_name_plural = 'операции'

    def __str__(self):
        return f'{self.title} ({self.user.username})'


class Order(models.Model):
    """Заказ - наряд"""
    @staticmethod
    def generate_code():
        last_order = Order.objects.order_by('accept_date').last()
        return f"{int(last_order.code) + 1}"

    def sum_operation(self):
        cost_operation = 0

        if self.count_of_cylinders != 0:
            operations = self.operation.filter(category__title='Блок')
            for operation in operations:
                print(operation.price)
                cost_operation += operation.price * self.count_of_cylinders

            return cost_operation

        if self.count_of_valves != 0:
            operations = (self.operation.objects.filter(category__title='ГБЦ'))
            for operation in operations:
                cost_operation = operation.price * self.count_of_valves

            return cost_operation

    code = models.CharField('Номер заказа',
                            max_length=255,
                            db_index=True,
                            default=generate_code,
                            )
    customer_name = models.CharField('Имя заказчика', max_length=50)
    customer_phone_number = models.CharField('Номер заказчика', max_length=12)
    engine_title = models.CharField('Наименование двигателя', max_length=50)
    accept_date = models.DateTimeField('Дата приёма', auto_now=True)
    count_of_cylinders = models.IntegerField('Количество цилиндров', default=0)
    count_of_valves = models.IntegerField('Количество клапанов', default=0)
    operation = models.ManyToManyField(Operation,
                                       verbose_name='Операция',
                                       related_name='task'
                                       )
    total_amount = models.PositiveIntegerField('Итоговая сумма', default=0)
    comments = models.TextField('Комментарии', blank=True, null=True)
    complete_date = models.DateTimeField('Дата выполнения',
                                         blank=True,
                                         null=True)

    class Meta:
        ordering = ['-accept_date']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.code + ' ' + self.customer_name

    def save(self, *args, **kwargs):
        self.total_amount = self.sum_operation()
        super().save(*args, **kwargs)

