from datetime import datetime

from django.db import models


class Author(models.Model):

    screen_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField()
    user = models.ForeignKey('auth.User', blank=True, null=True, unique=True)

    #profile_image_url = ...
    #lang = ...
    #profile_design = ...
    #utc_offset = ...
    #time_zone = ...

    def __unicode__(self):
        return u'%s (%s)' % (self.screen_name, self.display_name)


class Status(models.Model):

    author = models.ForeignKey(Author)
    text = models.TextField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)

    in_reply_to = models.ForeignKey('Status', blank=True, null=True, related_name='replies')
    conversation = models.ForeignKey('Status', blank=True, null=True, related_name='conversation_replies')

    def __unicode__(self):
        return u'%s: "%s"' % (self.author.screen_name, self.text[:100])

    class Meta:
        verbose_name_plural = 'statuses'


class StreamWhy(models.Model):

    actor = models.ForeignKey(Author)
    verb = models.CharField(max_length=100)


class UserStream(models.Model):

    user = models.ForeignKey('auth.User')
    status = models.ForeignKey(Status)
    display_at = models.DateTimeField()
    why = models.ForeignKey(StreamWhy, blank=True, null=True)

    def __unicode__(self):
        return u'%r for %s at %s' % (self.status, self.user.username, self.display_at.isoformat(' '))
