from django.db import models
import os

class Template(models.Model):
    name = models.CharField(max_length=255)
    cover_part = models.ForeignKey(
        'TemplatePart',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_as_cover_for'
    )

    def __str__(self):
        return self.name

class TemplatePart(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='parts')
    name = models.CharField(max_length=255, blank=True)
    html_file = models.FileField(upload_to='templates_parts/html/')
    thumbnail = models.ImageField(upload_to='templates_parts/thumbnails/')

    def save(self, *args, **kwargs):
        if not self.name:
            filename = os.path.basename(self.html_file.name)
            name_without_ext = os.path.splitext(filename)[0]
            self.name = name_without_ext
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.template.name} - {self.name}"
