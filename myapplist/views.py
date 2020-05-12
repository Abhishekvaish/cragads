from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from  bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

def base(request):
	return render(request, 'myapplist/base.html')


def new_search(request)	:
	search=request.POST.get('search')
	print(search)
	Search.objects.create(search_field=search)

	return HttpResponseRedirect(reverse('myapplist:index',args=(search,) )) 


def index(request,query):
	url = f'https://mumbai.craigslist.org/search/?query={ quote_plus(query) }'
	response = requests.get(url)

	img_url = 'https://images.craigslist.org/{}_300x300.jpg'

	soup = BeautifulSoup(response.text,features='html.parser')
	topics=[]

	for topic in soup.find_all('li',{'class':'result-row'}):
		title = topic.find('a',{'class':'result-title'}).get_text()
		link = topic.find('a',{'class':'result-title'}).get('href')
		if topic.find('a',{'class':'result-image'}).get('data-ids'):
			imgid = topic.find('a',{'class':'result-image'}).get('data-ids').split(',')[0].split(':')[1]
			img = img_url.format(imgid)
		else :
			img = 'https://craigslist.org/images/peace.jpg'
		topics.append((title,link,img))

	context = {
		'search':query,
		'topics':topics,
	}
	return render(request, 'myapplist/index.html',context)

