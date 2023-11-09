from django.contrib import admin

from .models import Marker, Comment

# Register your models here.
admin.site.register(Marker)
admin.site.register(Comment)