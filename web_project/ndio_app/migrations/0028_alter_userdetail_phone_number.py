# Generated by Django 5.1.4 on 2025-03-12 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndio_app", "0027_alter_fibreproduct_product_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetail",
            name="phone_number",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
