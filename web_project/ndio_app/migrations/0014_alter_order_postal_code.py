# Generated by Django 5.1.4 on 2025-01-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndio_app', '0013_alter_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.IntegerField(max_length=4),
        ),
    ]
