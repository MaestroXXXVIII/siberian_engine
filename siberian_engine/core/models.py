from django.db import models
from django.utils import timezone


class CarBrand(models.Model):
    title = models.CharField('Название', max_length=50)

    class Meta:
        ordering = ['title']
        verbose_name = 'брэнд автомобиля'
        verbose_name_plural = 'брэнды автомобиля'

    def __str__(self):
        return self.title


class Engine(models.Model):

    TRUCK_ENGINE = 'TE'
    CAR = 'C'
    ENGINE_TYPE = (
        (TRUCK_ENGINE, "Truck Engine"),
        (CAR, "Car")
    )
    brand = models.ForeignKey(CarBrand, verbose_name="Брэнд",
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                              )
    title = models.CharField("Название", max_length=100)
    count_of_cylinders = models.IntegerField("Количество цилиндров", default=0)
    count_of_valves = models.IntegerField("Количество клапанов", default=0)
    engine_type = models.CharField("Тип двигателя", choices=ENGINE_TYPE)

    class Meta:
        verbose_name = 'двигатель'
        verbose_name_plural = 'двигатели'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['engine_type']),
        ]

    def __str__(self):
        return f'{self.brand} {self.title}'


class CategoryOperations(models.Model):
    title = models.CharField("Название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.title


class Operation(models.Model):
    """Технологическая операция"""

    title = models.CharField("Название", max_length=125)
    category = models.ForeignKey(CategoryOperations,
                                 verbose_name="Категория",
                                 on_delete=models.CASCADE
                                 )
    engine = models.ForeignKey(Engine,
                               verbose_name="Двигатель",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True
                               )
    price = models.PositiveIntegerField("Цена")

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['engine'])
        ]
        verbose_name = "операция"
        verbose_name_plural = "операции"

    def __str__(self):
        return f"{self.title} ({self.engine})"


class Order(models.Model):
    """Заказ - наряд"""
    STATUS_ACCEPT = 'Принят'
    STATUS_IN_PROGRESS = 'В работе'
    STATUS_COMPLETE = 'Готов'

    STATUS_ORDER = (
        (STATUS_ACCEPT, 'Принят'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_COMPLETE, 'Готов')
    )

    id = models.AutoField("Номер заказа", primary_key=True, unique=True)
    customer_name = models.CharField("Имя заказчика", max_length=50)
    customer_phone_number = models.CharField("Номер заказчика", max_length=12)
    customer_email = models.EmailField("Почта",
                                       max_length=100,
                                       blank=True,
                                       null=True
                                       )
    engine = models.ForeignKey(Engine,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    operation = models.ManyToManyField(Operation,
                                       verbose_name="Операция",
                                       related_name="task"
                                       )
    total_amount = models.PositiveIntegerField("Итоговая сумма", default=0)
    comments = models.TextField("Комментарии", blank=True, null=True)
    accept_date = models.DateTimeField("Дата приёма", default=timezone.now())
    complete_date = models.DateTimeField("Дата выполнения",
                                         blank=True,
                                         null=True
                                         )
    status = models.CharField('Статус заказа',
                              choices=STATUS_ORDER,
                              default=STATUS_ORDER[0])

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['customer_name']),
            models.Index(fields=['engine'])
        ]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f'{self.id} {self.customer_name}'
