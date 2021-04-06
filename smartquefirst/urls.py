from django.urls import path
 
from . import views
app_name = 'smartquefirst'
 
urlpatterns = [
	path('', views.index, name='index'),
	path('topics/<int:topic_id>/', views.topic, name='topic'),
]