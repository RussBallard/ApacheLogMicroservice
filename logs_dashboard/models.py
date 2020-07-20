from django.db import models


# Если встречается неоправдано большая вместительность поля, то это для строчек с попыткой взлома
class LogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    method = models.CharField(max_length=1500)
    request_path = models.CharField(max_length=1000)
    http_version = models.CharField(max_length=5)
    status_code = models.CharField(max_length=3)
    response_size = models.PositiveIntegerField(default=0)
    referrer = models.CharField(max_length=1000)
    user_agent = models.CharField(max_length=300)

    def __str__(self):
        return self.id
