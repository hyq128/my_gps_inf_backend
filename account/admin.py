from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from .models import CustomUser, LocationInf, AccelerometerInf, BlueToothInf, gps_cluster,bt_cluster

@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Add additional fields to user admin page."""
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "device", "phone_number", "gender", "exp_id", "exp_name", "exp_state")}),
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
    actions = ['delete_selected']  # Ensure bulk delete is enabled

class GroupProxy(Group):
    """Proxy model for Group. Dedicated for django-admin."""
    class Meta:
        """Declare model being proxy."""
        proxy = True
        verbose_name_plural = verbose_name = '用户组'

@admin.register(GroupProxy)
class MyGroupAdmin(DjangoGroupAdmin):
    """Grouping useradmin with groupadmin"""
    actions = ['delete_selected']  # Ensure bulk delete is enabled

admin.site.unregister(Group)  # Avoid multiple GroupAdmin

class LocationAdmin(admin.ModelAdmin):
    fields = ('username', 'device', 'longitude', 'latitude', 'accuracy')
    list_display = ('username', 'device', 'longitude', 'latitude', 'accuracy', 'timestamp', 'label')
    search_fields = ['username']
    list_per_page = 20
    actions = ['delete_selected']  # Ensure bulk delete is enabled

admin.site.register(LocationInf, LocationAdmin)

class BlueToothAdmin(admin.ModelAdmin):
    fields = ('username', 'device', 'connection_device')
    list_display = ('username', 'device', 'connection_device', 'timestamp')
    search_fields = ['username']
    list_per_page = 6
    actions = ['delete_selected']  # Ensure bulk delete is enabled

admin.site.register(BlueToothInf, BlueToothAdmin)

class AccelerometerAdmin(admin.ModelAdmin):
    fields = ('username', 'device', 'acc_x', 'acc_y', 'acc_z')
    list_display = ('username', 'device', 'acc_x', 'acc_y', 'acc_z', 'timestamp')
    search_fields = ['username']
    list_per_page = 20
    actions = ['delete_selected']  # Ensure bulk delete is enabled

admin.site.register(AccelerometerInf, AccelerometerAdmin)

class gps_clusterAdmin(admin.ModelAdmin):
    fields = ('username', 'cluster_name', 'longitude', 'latitude')
    list_display = ('username', 'cluster_name', 'longitude', 'latitude', 'timestamp')
    search_fields = ['username']
    list_per_page = 20
    actions = ['delete_selected']  # Ensure bulk delete is enabled

admin.site.register(gps_cluster, gps_clusterAdmin)


class bt_clusterAdmin(admin.ModelAdmin):
    fields = ('username', 'label', 'bt_device')
    list_display = ('username', 'label','bt_device')
    search_fields = ['username']
    list_per_page = 20
    actions = ['delete_selected']  # Ensure bulk delete is enabled
admin.site.register(bt_cluster, bt_clusterAdmin)