from django.shortcuts import render
from .models import Topic
from django.contrib.auth.decorators import login_required
from django.http import Http404
import requests
import json


def index(request):
    #response = requests.get("http://localhost:8000/api/smartquerest/")
    #jsonrequest = response.json()
    #topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {
        'title' : 'Главная страница'
	}
    return render(request, 'smartquefirst/main.html', context)


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


def schedule(request):
    firstline = ['Cab1', 'Cab2', 'Cab3']
    otherlines = [['1', '2', '3'], ['4', '-', '-']]
    context = {
        'title' : 'Текущая очередь',
        'firstths' : firstline,
        'trs' : otherlines
    }
    return render(request, 'smartquefirst/schedule.html', context)


def recording(request):
    response = requests.get("http://localhost:8000/api/smartquerest/cabinets_by_name/")
    response = response.text.replace('\\', '')
    checkboxes = json.loads(response[1:-1])
    print(response)
    print(checkboxes)
    checkboxes = checkboxes['cabs']
    context = {
        'title' : 'Запись',
        'checkboxes' : checkboxes
    }
    return render(request, 'smartquefirst/recording.html', context)


def yournumber(request):
    cabs_data = json.dumps(request.POST.getlist('cabs_options'))
    second = {'json_s' : cabs_data}
    clientnumber = requests.post("http://localhost:8000/api/smartquerest/create_guest/", data=second)
    context = {
        'title' : 'Результат записи',
        'clientnumber' : clientnumber.text
    }
    return render(request, 'smartquefirst/yournumber.html', context)