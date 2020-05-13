from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect,Http404
from django.utils import timezone
from  bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search
import re
space_remover = re.compile('\s+')


def base(request):
	return render(request, 'myapplist/base.html')


def new_search(request)	:
	search=request.POST.get('search')
	if search=='':
		return HttpResponseRedirect(reverse('myapplist:base'))
		

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
		l = topic.find('a',{'class':'result-title'}).get('href').split('/')
		link = l[2].split('.')[0]+'+'+ l[3]+'+'+l[5]+'+'+l[6].split('.')[0]

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


def detail(request,query):
	query =query.split('+')
	url = 'https://{}.craigslist.org/{}/d/{}/{}.html'.format(query[0],query[1],query[2],query[3])

	response = requests.get(url)
	soup = BeautifulSoup(response.text,features='html.parser')

	title = soup.find('h2',{'class':'postingtitle'}).get_text()
	title = space_remover.sub(" ",title)

	date = soup.find('p',{'id':'display-date'}).get_text()
	date = space_remover.sub(" ",date)

	body_text = soup.find('section',{'id':'postingbody'}).get_text().split('\n\n\n')[1]

	imgsrc = None
	if soup.find('div',{'class':'gallery'}):
		imgsrc = soup.find('div',{'class':'gallery'}).find('img').get('src')
		
	context = {
		'title':title,
		'date':date,
		'body_text':body_text,
		'imgsrc':imgsrc,
	}

	return render(request, 'myapplist/detail.html',context=context)




