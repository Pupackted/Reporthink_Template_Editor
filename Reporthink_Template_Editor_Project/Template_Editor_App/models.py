from django.db import models
import os
from django.contrib.auth.models import User

class Template(models.Model):
    name = models.CharField(max_length=255)
    cover_part = models.ForeignKey(
        'TemplatePart',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_as_cover_for'
    )

    def get_template_path(self):
        return f"templates_folder/{self.html_file}"

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



# save edits made by users to templates

# class UserTemplateEdit(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='template_edits')
#     template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='user_edits')
#     # Store all edited parts as JSON: {part_id: html_content, ...}
#     edited_parts = models.JSONField(default=dict)
#     last_modified = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.template.name} edit"


class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='user_documents')
    
    # This is the key field: a name for the user's specific version.
    name = models.CharField(max_length=255) 
    
    # This field moves from the old model to here.
    edited_parts = models.JSONField(default=dict) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"'{self.name}' by {self.user.username} (from: {self.template.name})"
