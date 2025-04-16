from django.db import models

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=255)
    html_file = models.FileField(upload_to='templates_to_be_edited/')
    thumbnail = models.ImageField(upload_to='templates_thumbnails/')

    def __str__(self):
        return self.name