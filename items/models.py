from django.db import models
from django.template.defaultfilters import truncatechars


class Item(models.Model):
    photo = models.ImageField(upload_to='items/photo')
    title = models.CharField(max_length=128)
    description = models.TextField()

    def short_description(self):
        return truncatechars(self.description, 35)
