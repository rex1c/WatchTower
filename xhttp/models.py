from django.db import models

class HTTPx(models.Model):
    programm_name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    ips = models.JSONField()
    tech = models.JSONField()
    favicon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    status_code = models.JSONField()
    headers = models.JSONField()
    url = models.CharField(max_length=255)
    final_url = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.programm_name