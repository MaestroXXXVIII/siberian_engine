# Generated by Django 4.2 on 2024-02-06 10:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_order_complete_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operation',
            options={'ordering': ['user']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-accept_date']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='complete_operation_date',
        ),
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(db_index=True, default=core.models.Order.generate_code, max_length=255),
        ),
    ]
