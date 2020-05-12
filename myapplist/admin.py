from django.contrib import admin
from .models import Search
# Register your models here.

class SearchAdmin(admin.ModelAdmin):
	list_display = ('search_field','created')
	fields = ['search_field']
	readonly_fields = ['created',]
	list_filter = ['created']


admin.site.register(Search,SearchAdmin)
