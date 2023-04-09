from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


# Create your models here.
class customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,default="", on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=20,null =  False,default="")
    address=models.CharField(max_length=20, null = False)
    pincode=models.IntegerField(null=False)
    phone_number=models.IntegerField(null=False)  
    def __str__(self):
        return self.customer_name   
    
class employee(models.Model):
    user=models.OneToOneField(User,default=None, on_delete=models.CASCADE)
    name=models.CharField(max_length=20,default="",null=True,blank=True)
    address=models.CharField(max_length=20,default="", null = False,)
    services=models.CharField(max_length=100,default="", null = True,blank=True)
    haircutting  = models.BooleanField(default=False, null=True)
    styling= models.BooleanField(default=False, null=True)
    threading= models.BooleanField(default=False,null=True)  
    waxing= models.BooleanField(default=False, null=True)
    manicure= models.BooleanField(default=False, null=True)
    pedicure= models.BooleanField(default=False,  null=True)
    rates=models.CharField(max_length=100,default="",null=False)
    image=models.ImageField(upload_to='shopImage',default="",null=True)   
    
class appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class shopapointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee=models.ForeignKey(employee, on_delete=models.CASCADE, default="")
    services = models.CharField(max_length=100)
    time = models.CharField(default="",max_length=20)
    confirm=models.BooleanField(default=False)