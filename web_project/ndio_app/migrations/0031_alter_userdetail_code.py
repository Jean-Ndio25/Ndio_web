# Generated by Django 5.1.4 on 2025-03-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndio_app", "0030_order_province"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetail",
            name="code",
            field=models.CharField(
                blank=True, editable=False, max_length=12, unique=True
            ),
        ),
    ]
