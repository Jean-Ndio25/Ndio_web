from django.contrib import admin
from ndio_app.models import User_Detail, Order, Payment

# Register your models here.
admin.site.register(User_Detail)
admin.site.register(Order)
admin.site.register(Payment)