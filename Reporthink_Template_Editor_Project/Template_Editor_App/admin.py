from django.contrib import admin
from .models import Template, TemplatePart, UserDocument

class TemplatePartInline(admin.TabularInline):
    model = TemplatePart
    extra = 1
    fields = ['html_file', 'thumbnail', 'name']
    readonly_fields = ['name']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplatePartInline]

    def get_exclude(self, request, obj=None):
        # on the ADD form (obj is None), hide the cover_part field
        if obj is None:
            return ('cover_part',)
        # on the CHANGE form, show it so you can override if you want
        return ()

# you can still register TemplatePart standalone if you like:
admin.site.register(TemplatePart)
@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    # This will show these fields as columns on the admin page
    list_display = ('name', 'user', 'template', 'last_modified')
    # This adds a search bar to search by these fields
    search_fields = ('name', 'user__username', 'template__name')
    # This adds filters to the right sidebar
    list_filter = ('user', 'template', 'last_modified')
    # Makes the JSON field easier to read
    readonly_fields = ('created_at', 'last_modified')
