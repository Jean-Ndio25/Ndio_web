# Generated by Django 5.1.4 on 2025-03-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndio_app", "0032_alter_order_client"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="suburb",
            field=models.CharField(default="null", max_length=150),
            preserve_default=False,
        ),
    ]
