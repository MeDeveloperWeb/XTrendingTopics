from django.contrib import admin
from .models import Auth, IP, Topic
# Register your models here.

admin.site.register(Auth)
admin.site.register(IP)
admin.site.register(Topic)