from django.contrib import admin
from ndio_app.models import UserDetail, Order, Payment, UserSubscription, FibreProduct, NetworkProvider, Communication

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(UserSubscription)
admin.site.register(FibreProduct)
admin.site.register(NetworkProvider)
admin.site.register(Communication)