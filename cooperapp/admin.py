from django.contrib import admin
from .models import UserProfile, RequestAjoAdminverification,RequestCopAdminverification

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RequestAjoAdminverification)
admin.site.register(RequestCopAdminverification)
