from django.contrib import admin

from .models import Forms, Horses, Jockeys, Tracks
# Register your models here.

admin.site.register(Forms)
admin.site.register(Horses)
admin.site.register(Jockeys)
admin.site.register(Tracks)