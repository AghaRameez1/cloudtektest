from django.db import models

# Create your models here.

class DataTable(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(default=0, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name