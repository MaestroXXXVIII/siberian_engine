# Generated by Django 4.2 on 2024-03-09 03:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_order_status_alter_engine_engine_type_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="carbrand",
            options={
                "ordering": ["title"],
                "verbose_name": "брэнд автомобиля",
                "verbose_name_plural": "брэнды автомобиля",
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ["-id"],
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
            },
        ),
        migrations.RemoveField(
            model_name="categoryoperations",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="engine",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="operation",
            name="slug",
        ),
        migrations.AlterField(
            model_name="order",
            name="accept_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 9, 3, 14, 25, 462077, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата приёма",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Принят", "Принят"),
                    ("В работе", "В работе"),
                    ("Готов", "Готов"),
                ],
                default=("Принят", "Принят"),
                verbose_name="Статус заказа",
            ),
        ),
    ]
