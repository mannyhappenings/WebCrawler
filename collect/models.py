from django.db import models


class HtmlCollection(models.Model):
	url = models.CharField(unique=True, max_length=100)
	text = models.TextField()

