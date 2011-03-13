from datetime import datetime

from django.db import models
import django_push.subscriber.signals


class Author(models.Model):

    atom_id = models.CharField(max_length=200, unique=True)
    screen_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    homepage_url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey('auth.User', blank=True, null=True, unique=True)

    #profile_image_url = ...
    #lang = ...
    #profile_design = ...
    #utc_offset = ...
    #time_zone = ...

    def __unicode__(self):
        return u'%s (%s)' % (self.screen_name, self.display_name)


class Status(models.Model):

    atom_id = models.CharField(max_length=200)
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


def yo_hay(notification, **kwargs):
    import logging
    from pprint import pformat
    logging.getLogger(__name__).debug(pformat(notification))

def save_items(notification, **kwargs):
    for feedentry in notification.entries:
        # TODO: is this publisher authoritative for this atom id?
        atom_id = feedentry.id
        try:
            status = Status.objects.get(atom_id=atom_id)
        except Status.DoesNotExist:
            status = Status(atom_id=atom_id)

        # TODO: try content first if there ever is one
        status.text = feedentry.summary

        # TODO: try entry author if there ever is one
        feed = notification.feed
        author_url = feed.author_detail.href
        try:
            author = Author.objects.get(url=author_url)
        except Author.DoesNotExist:
            author = Author(url=author_url)

        author.screen_name = feed.poco_preferredusername
        author.display_name = feed.poco_displayname
        author.location = feed.formatted  # ?!
        #author.description = feed.butt
        author.save()

        status.author = author
        status.save()

django_push.subscriber.signals.updated.connect(yo_hay)
django_push.subscriber.signals.updated.connect(save_items)
