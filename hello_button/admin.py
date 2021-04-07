from django.contrib import admin
from .models import LabMembers

# Register your models here.

# Register your models here.
@admin.register(LabMembers)
class LabMembersAdmin(admin.ModelAdmin):
    list_display = ('name',)
