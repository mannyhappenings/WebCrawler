from django.shortcuts import render
from crawler import Crawler
from django.http import HttpResponse

crawlers = {}

def index(request, params=''):
	post_data = dict(request.POST)
	post_data['urls'] = post_data['url[]']
	for link in post_data['urls']:
	    crawlers[link] = Crawler()
	    
	    crawlers[link].setUrl(link)
	    crawlers[link].start()

		
		
	return render(request, 'crawl/index.html', {'urls': post_data['urls']})

def status(request):
	response_text = "Total documents collected: <span class='count'>" + str(Crawler.crawledUrls['size']) + "</span>"
	return HttpResponse(str(response_text))
	
def stop(request):
	for key in crawlers.keys():
		crawlers[key].stop()
		
	response_text = "Stopped"
	return HttpResponse(response_text)