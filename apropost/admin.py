from django.contrib import admin

from apropost.models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'display_name', 'url', 'created_at', 'user')

admin.site.register(Author, AuthorAdmin)


admin.site.register(Status)
admin.site.register(StreamWhy)
admin.site.register(UserStream)
