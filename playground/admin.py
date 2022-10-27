from django.contrib import admin
from .models import WebsiteUser
from .models import Info, Pages

# Register your models here.

admin.site.register(WebsiteUser)
admin.site.register(Info)
admin.site.register(Pages)


