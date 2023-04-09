from django.contrib import admin
from .models import customer,employee,appointment,shopapointment

# Register your models here.
admin.site.register(customer)
admin.site.register(employee)
admin.site.register(appointment)
admin.site.register(shopapointment)