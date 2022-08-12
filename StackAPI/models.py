from django.db import models

# Create your models here.
class Link(models.Model):
    url=models.TextField(null=True)

    def __str__(self):
        return self.url

class Data(models.Model):
    dt=models.TextField(null=True)

    def __str__(self):
         return self.dt

class Tag(models.Model):
    tags=models.CharField(max_length=500)
    
    def __str__(self):
         return self.tags
