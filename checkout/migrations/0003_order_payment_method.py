# Generated by Django 5.0.1 on 2024-02-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_address_order_email_order_name_order_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('CC', 'Credit Card'), ('PP', 'PayPal'), ('COD', 'Cash on Delivery')], default='CC', max_length=3),
        ),
    ]
