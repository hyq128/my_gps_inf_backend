from django.contrib import admin
from django.contrib.auth.admin import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from .models import CustomUser
from .models import LocationInf,AccelerometerInf,BlueToothInf
from django.utils.html import format_html
from django.utils.safestring import mark_safe, SafeText
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Add additional fields to user admin page."""
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name","email","device","phone_number","gender")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email")


class GroupProxy(Group):
    """Proxy model for Group. Dedicated for django-admin."""
    class Meta:
        """Declare model being proxy."""
        proxy = True
        verbose_name_plural = verbose_name = '用户组'


@admin.register(GroupProxy)
class MyGroupAdmin(DjangoGroupAdmin):
    """Grouping useradmin with groupadmin"""


admin.site.unregister(Group)  # Avoid multiple GroupAdmin



# #用户信息管理：
class LocationAdmin(admin.ModelAdmin):
    fields=('username','device','longitude','latitude')
    list_display=('username','device','longitude','latitude','timestamp')
    # 要搜索的列的值 
    search_fields = ['username']
    list_per_page = 20
admin.site.register(LocationInf,LocationAdmin)


class BlueToothAdmin(admin.ModelAdmin):
    fields=('username','device','connection_device')
    list_display=('username','device','connection_device','timestamp')
    # 要搜索的列的值 
    search_fields = ['username']
    list_per_page = 6
admin.site.register(BlueToothInf,BlueToothAdmin)


class AccelerometerAdmin(admin.ModelAdmin):
    fields=('username','device','acc_x','acc_y','acc_z')
    list_display=('username','device','acc_x','acc_y','acc_z','timestamp')
    # 要搜索的列的值 
    search_fields = ['username']
    list_per_page = 20
admin.site.register(AccelerometerInf,AccelerometerAdmin)