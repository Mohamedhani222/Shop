# Generated by Django 4.0.6 on 2022-08-15 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgapp', '0034_alter_order_orderdate_alter_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 15, 19, 16, 28, 892263)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 15, 19, 16, 28, 893263), null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='createdat',
            field=models.DateField(default=datetime.datetime(2022, 8, 15, 19, 16, 28, 891263)),
        ),
    ]
