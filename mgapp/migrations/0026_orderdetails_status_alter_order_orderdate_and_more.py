# Generated by Django 4.0.6 on 2022-08-15 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mgapp', '0025_payment_date_alter_order_orderdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('Deliverd', 'Deliverd'), ('Out for delivery', 'Out for delivery'), ('Canceled', 'Canceled')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 15, 16, 54, 9, 695314)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 8, 15, 16, 54, 9, 696312), null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='createdat',
            field=models.DateField(default=datetime.datetime(2022, 8, 15, 16, 54, 9, 695314)),
        ),
        migrations.DeleteModel(
            name='confirm',
        ),
    ]
