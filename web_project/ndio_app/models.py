import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_Detail(models.Model):
    id_number = models.CharField(primary_key=True, max_length= 15)
    phone_number = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_details")
    code = models.CharField(max_length=12, unique=True,blank=True)
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Set a unique referral code if one doesn't exist.
        """

        if not self.code:
            self.code = str(uuid.uuid4())[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    address_type = models.CharField(max_length=30)
    apartment_name = models.CharField(max_length=30, null=True, blank=True) # This field can be empty
    apartment_floor = models.IntegerField(null=True, blank=True)
    apartment_unit = models.IntegerField(null=True, blank=True)
    estate_name = models.CharField(max_length=30, null=True, blank=True)
    estate_address = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    postal_code = models.IntegerField()
    id_number = models.ForeignKey(User_Detail, on_delete=models.CASCADE) 


class Payment(models.Model):
    payment_id = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
