from django.contrib import admin
from .models import User, DeviceGroup
from .models import Device, Parameter, SentData, DataFrame

# Register your models here.
admin.site.register(User)
admin.site.register(DeviceGroup)
admin.site.register(Device)
admin.site.register(Parameter)
admin.site.register(SentData)
admin.site.register(DataFrame)

