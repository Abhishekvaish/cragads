from django.urls import path
from . import views


app_name = 'myapplist'

urlpatterns = [
	# www.mywesite.com
	path('', views.base,name='base'),

	# www.mysite.com/new_search
	path('new_search', views.new_search,name='new_search'),

	path('query?=<str:query>', views.index,name='index'),

]