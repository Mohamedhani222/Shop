# Generated by Django 4.1.1 on 2022-09-07 03:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mgapp', '0049_product_description_alter_order_orderdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 5, 31, 1, 122323)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 7, 5, 31, 1, 123324), null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='createdat',
            field=models.DateField(default=datetime.datetime(2022, 9, 7, 5, 31, 1, 121324)),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=2000)),
                ('createdat', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('closed', 'closed'), ('pending', 'pending'), ('answerd', 'answerd')], max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Responseticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res', models.TextField(max_length=2000)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgapp.ticket')),
            ],
        ),
    ]
