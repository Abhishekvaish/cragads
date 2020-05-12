from django.db import models

# Create your models here.
# python manage.py makemigrations myapplist
# python manage.py migrate
# python manage.py sqlmigrate myapplist 0001

class Search(models.Model):
	search_field = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'Searches'

	def __str__(self):
		return self.search_field