# Generated by Django 3.1.7 on 2021-05-02 11:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210427_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address')),
                ('status', models.CharField(choices=[('new', 'New order'), ('in_progress', 'Order in progress'), ('is_ready', 'Order is ready'), ('completed', 'Order completed')], default='new', max_length=100, verbose_name='Order status')),
                ('buying_type', models.CharField(choices=[('self', 'Pickup'), ('delivery', 'Delivery')], default='self', max_length=100, verbose_name='Order type')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Order comment')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('order_date', models.DateField(default=django.utils.timezone.now, verbose_name='Date of receipt of the order')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='mainapp.customer', verbose_name='Customer')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_customer', to='mainapp.Order', verbose_name='Customer orders'),
        ),
    ]
