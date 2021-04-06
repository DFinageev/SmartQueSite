from django.shortcuts import render
from .models import Topic
from django.contrib.auth.decorators import login_required
from django.http import Http404
import requests
 
@login_required
def index(request):
    response = requests.get("http://localhost:8000/api/smartquerest/")
    jsonrequest = response.json()
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {
		'topics': topics,
        'jsonrequest': jsonrequest
	}
    return render(request, 'smartquefirst/index.html', context)
 
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {
    	'topic': topic,
    	'entries': entries,
	}
    return render(request, 'smartquefirst/topic.html', context)