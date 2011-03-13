from django.contrib import admin

from apropost.models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('screen_name', 'display_name', 'url', 'created_at', 'user')

admin.site.register(Author, AuthorAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'author__screen_name', 'created_at', 'text', 'source')

    def author__screen_name(self, obj):
        return obj.author.screen_name

admin.site.register(Status, StatusAdmin)


admin.site.register(StreamWhy)


class UserStreamAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'display_at', 'why')

    def why(self, obj):
        if obj.why is None:
            return None
        return u'%s by %s' % (obj.why.verb, obj.why.actor.screen_name)

admin.site.register(UserStream, UserStreamAdmin)
