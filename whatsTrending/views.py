from django.shortcuts import render
from whatsTrending.utils import getTrendingData
from uuid import uuid4
from .models import IP, Topic

# Create your views here.
def index(request):
	ip = {}
	currentTopics = []
	error = False
	exception = ''

	try:
		data = getTrendingData()

		ip = IP(id=uuid4(), ip=data['ip'])
		ip.save()

		for topic in data["topics"]:
			currentTopics.append(topic)
			Topic(content=topic, ip=ip).save()

	except Exception as e:
		error = True
		exception = e
		print(e)

	jsonData = []

	for ip in IP.objects.all():
		topics = []
		for topic in ip.topics.all():
			topics.append(topic.content)
		
		jsonData.append({
			"id": ip.id,
			"topics": topics
		})

	return render(request, 'index.html', {
		"datetime": ip.dateTime,
		"ip": ip.ip,
		"currentTopics": currentTopics,
		"jsonData": jsonData,
		"error": error,
		"exception": exception
	})