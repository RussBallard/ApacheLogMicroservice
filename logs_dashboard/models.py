from django.db import models


class LogEntry(models.Model):
    ip = models.CharField(max_length=300)
    date = models.CharField(max_length=300)
    method = models.CharField(max_length=300)
    request_path = models.CharField(max_length=1000)
    http_version = models.CharField(max_length=300)
    status_code = models.IntegerField()
    response_size = models.IntegerField()
    referrer = models.CharField(max_length=1000)
    user_agent = models.CharField(max_length=300)
