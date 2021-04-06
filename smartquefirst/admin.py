from django.contrib import admin
from .models import Topic, Entry
 
admin.site.register(Entry)
 
class TopicAdmin(admin.ModelAdmin):
	readonly_fields=('owner', )
 
	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		obj.save()
 
admin.site.register(Topic, TopicAdmin)