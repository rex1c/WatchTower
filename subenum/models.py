from django.db import models

class Subdomains(models.Model):
    programm_name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    providers = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.programm_name