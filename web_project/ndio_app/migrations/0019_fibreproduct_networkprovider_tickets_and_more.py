# Generated by Django 5.1.4 on 2025-03-07 11:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ndio_app", "0018_alter_user_detail_created_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FibreProduct",
            fields=[
                (
                    "product_id",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                ("product_name", models.CharField(max_length=100)),
                (
                    "price",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=10),
                ),
                ("slug", models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="NetworkProvider",
            fields=[
                (
                    "guid_network_provider_id",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Tickets",
            fields=[
                ("ticket_id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name="order",
            name="id_number",
        ),
        migrations.AddField(
            model_name="order",
            name="client",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="date_completed",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="order_complete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="payment",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="order",
            name="apartment_floor",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="apartment_unit",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="postal_code",
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name="payment",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Communication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message_type",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("sms", "SMS"),
                            ("notification", "Notification"),
                        ],
                        max_length=20,
                    ),
                ),
                ("message_subject", models.CharField(max_length=100)),
                ("date_sent", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "message_receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="ordered_product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order",
                to="ndio_app.fibreproduct",
            ),
        ),
        migrations.AddField(
            model_name="fibreproduct",
            name="network_provider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="ndio_app.networkprovider",
            ),
        ),
        migrations.CreateModel(
            name="UserDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "phone_number",
                    models.CharField(
                        max_length=10, unique=True
                    ),
                ),
                ("id_number", models.CharField(max_length=15, unique=True)),
                (
                    "code",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "referred_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserSubscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")],
                        max_length=10,
                    ),
                ),
                ("activation_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("payment_due_date", models.DateTimeField(null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to="ndio_app.fibreproduct",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscription",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="User_Detail",
        ),
    ]
