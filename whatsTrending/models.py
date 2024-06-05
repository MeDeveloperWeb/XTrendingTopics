from django.db import models
from django.utils import timezone

# Create your models here.
class IP(models.Model):
	id = models.UUIDField(primary_key=True, editable=False)
	ip = models.CharField(max_length=50)
	dateTime = models.DateTimeField(default=timezone.now)

class Topic(models.Model):
	ip = models.ForeignKey(IP, related_name='topics', on_delete=models.CASCADE)
	content = models.CharField(max_length=128)

class Auth(models.Model):
	cookie = models.JSONField()