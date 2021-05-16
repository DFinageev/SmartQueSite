from django.contrib import admin

from .models import Guest, Cabinet, MovedGuest


admin.site.register(Guest)
admin.site.register(Cabinet)
admin.site.register(MovedGuest)
#admin.site.register(Schedule)
