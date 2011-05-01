from django.contrib import admin

from apropost.models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'atom_id', 'created_at')

admin.site.register(Author, AuthorAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author__screen_name', 'created', 'published', 'text', 'source')

    def author__screen_name(self, obj):
        return obj.author.screen_name

admin.site.register(Post, PostAdmin)


admin.site.register(StreamWhy)


class UserStreamAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'display_at', 'why')

    def why(self, obj):
        if obj.why is None:
            return None
        return u'%s by %s' % (obj.why.verb, obj.why.actor.screen_name)

admin.site.register(UserStream, UserStreamAdmin)
