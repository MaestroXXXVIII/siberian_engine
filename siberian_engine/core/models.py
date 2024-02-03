from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)

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

    def __str__(self):
        return self.title


class Order(models.Model):
    """Заказ - наряд"""
    code = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=50)
    customer_phone_number = models.CharField(max_length=12)
    engine_title = models.CharField(max_length=50)
    accept_date = models.DateTimeField(auto_now=True)
    complete_date = models.DateTimeField()
    operation = models.ManyToManyField(Operation, related_name='task')
    complete_operation_date = models.DateTimeField()
    count_of_cylinders = models.IntegerField(default=0)
    count_of_valves = models.IntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code + ' ' + self.customer_name

    def sum_operation(self):
        cost_operation = 0

        if self.count_of_cylinders != 0:
            operations = self.operation.objects.exclude(category__title='Блок')
            for operation in operations:
                cost_operation = operation.price * self.count_of_cylinders
            return cost_operation

        if self.count_of_valves != 0:
            operations = self.operation.objects.exclude(category__title='ГБЦ')
            for operation in operations:
                cost_operation = operation.price * self.count_of_valves
            return cost_operation

    def sum_total_amount(self):
        operations = self.operation.objects.all()
        total_amount = self.total_amount
        for operation in operations:
            operation.price += total_amount

        return total_amount
