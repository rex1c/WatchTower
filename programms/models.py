from django.db import models

class Programm(models.Model):
    programm_name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    config = models.JSONField()
    scopes = models.JSONField()
    ooscopes = models.JSONField()

    def __str__(self):
        return self.programm_name