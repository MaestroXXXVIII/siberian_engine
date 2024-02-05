from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Operation(models.Model):
    """Технологическая операция"""
    title = models.CharField(max_length=125)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


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

    code = models.CharField(max_length=255,
                            db_index=True,
                            default=generate_code,
                            )
    customer_name = models.CharField(max_length=50)
    customer_phone_number = models.CharField(max_length=12)
    engine_title = models.CharField(max_length=50)
    accept_date = models.DateTimeField(auto_now=True)
    complete_date = models.DateTimeField(blank=True, null=True)
    operation = models.ManyToManyField(Operation, related_name='task')
    count_of_cylinders = models.IntegerField(default=0)
    count_of_valves = models.IntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-accept_date']

    def __str__(self):
        return self.code + ' ' + self.customer_name

    def save(self, *args, **kwargs):
        self.total_amount = self.sum_operation()
        super().save(*args, **kwargs)

