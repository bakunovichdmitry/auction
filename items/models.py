from django.db import models

class Item(models.Model):
    photo = models.ImageField(upload_to='items')
    title = models.CharField(max_length=128)
    description = models.TextField()
