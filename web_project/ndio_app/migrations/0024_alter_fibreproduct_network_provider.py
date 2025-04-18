# Generated by Django 5.1.4 on 2025-03-10 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndio_app", "0023_alter_fibreproduct_product_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fibreproduct",
            name="network_provider",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="ndio_app.networkprovider",
            ),
        ),
    ]
