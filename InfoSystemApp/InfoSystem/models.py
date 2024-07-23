from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', unique=True)
    password = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    salt = models.CharField(max_length=128, db_collation='utf8mb3_general_ci')
    email = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    info = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = UserManager()

    class Meta:
        db_table = 'Users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        managed = True


class DeviceGroup(models.Model):
    device_group_id = models.AutoField(primary_key=True, editable=False)
    device_group_name = models.CharField(max_length=50, db_collation='utf8mb3_general_ci')
    user = models.ForeignKey(User, models.DO_NOTHING)
    status = models.CharField(max_length=15, db_collation='utf8mb3_general_ci')
    creation_date = models.DateTimeField()
    description = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        db_table = 'DeviceGroups'
        verbose_name = 'DeviceGroup'
        verbose_name_plural = 'DeviceGroups'

class Device(models.Model):
    device_id = models.AutoField(primary_key=True, editable=False)
    device_name = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    device_group = models.ForeignKey(DeviceGroup, models.DO_NOTHING)
    authentication_token = models.CharField(max_length=128, db_collation='utf8mb3_general_ci', blank=True, null=True)
    creation_date = models.DateTimeField()
    status = models.CharField(max_length=15, db_collation='utf8mb3_general_ci')
    last_activity_time = models.DateTimeField()
    location_name = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    location_latitude = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    location_longtitude = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    location_timestamp = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        db_table = 'Devices'
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


class Parameter(models.Model):
    parameter_id = models.AutoField(primary_key=True, editable=False)
    parameter_name = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    parameter_symbol = models.CharField(max_length=25, db_collation='utf8mb3_general_ci')
    device = models.ForeignKey(Device, models.DO_NOTHING)

    class Meta:
        db_table = 'Parameters'
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'


class DataFrame(models.Model):
    data_frame_id = models.AutoField(primary_key=True, editable=False)
    parameter = models.ForeignKey(Parameter, models.DO_NOTHING)
    timestamp = models.DateTimeField()
    result = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    description = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        db_table = 'DataFrames'
        verbose_name = 'DataFrame'
        verbose_name_plural = 'DataFrames'


class SentData(models.Model):
    sent_data_id = models.AutoField(primary_key=True, editable=False)
    parameter = models.ForeignKey(Parameter, models.DO_NOTHING)
    timestamp = models.DateTimeField()
    value = models.CharField(max_length=254, db_collation='utf8mb3_general_ci')
    description = models.CharField(max_length=254, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        db_table = 'SentData'
        verbose_name = 'SentData'
        verbose_name_plural = 'SentData'
