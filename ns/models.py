from django.db import models

class LiveSubdomains(models.Model):
    programm_name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    cdn = models.BooleanField(default=False)
    ips = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.programm_name