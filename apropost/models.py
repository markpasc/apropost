from datetime import datetime
from xml.etree import ElementTree

from django.contrib.auth.models import User
from django.db import models
import django_push.subscriber.signals
import iso8601


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
    xml = ElementTree.tostring(notification, encoding='utf-8')
    logging.getLogger(__name__).debug(xml)

def save_items(notification, **kwargs):
    # TODO: handle entry level authors?
    author_el = notification.find('{http://www.w3.org/2005/Atom}author')
    author_id = author_el.findtext('{http://www.w3.org/2005/Atom}uri')
    try:
        author = Author.objects.get(atom_id=author_id)
    except Author.DoesNotExist:
        author = Author(atom_id=author_id)

    author.screen_name = author_el.findtext('{http://portablecontacts.net/spec/1.0}preferredUsername')
    author.display_name = author_el.findtext('{http://portablecontacts.net/spec/1.0}displayName')
    #author.description = ...?
    author.location = author_el.findtext('{http://portablecontacts.net/spec/1.0}address/{http://portablecontacts.net/spec/1.0}formatted')
    # ugh homepage url
    for url_el in author_el.findall('{http://portablecontacts.net/spec/1.0}urls'):
        if url_el.findtext('{http://portablecontacts.net/spec/1.0}type') in ('home', 'homepage') and url_el.findtext('{http://portablecontacts.net/spec/1.0}primary') == 'true':
            author.homepage_url = url_el.findtext('{http://portablecontacts.net/spec/1.0}value')

    author.save()

    for entry_el in notification.findall('{http://www.w3.org/2005/Atom}entry'):
        # TODO: care about things other than notes?
        if entry_el.findtext('{http://activitystrea.ms/spec/1.0/}object-type') != 'http://activitystrea.ms/schema/1.0/note':
            continue
        # TODO: care about activity other than posts
        if entry_el.findtext('{http://activitystrea.ms/spec/1.0/}verb') != 'http://activitystrea.ms/schema/1.0/post':
            continue

        # TODO: is this publisher authoritative for this atom id?
        atom_id = entry_el.findtext('{http://www.w3.org/2005/Atom}id')
        try:
            status = Status.objects.get(atom_id=atom_id)
        except Status.DoesNotExist:
            status = Status(atom_id=atom_id)

        # TODO: try content first if there ever is one
        content = entry_el.find('{http://www.w3.org/2005/Atom}content')
        content_type = content.get('type', 'html')
        if content_type == 'html':
            status.text = content.text
        else:
            raise ValueError("Unsupported content element type %r" % content_type)

        notice_info = entry_el.find('{http://status.net/schema/api/1/}notice_info')
        if notice_info is not None:
            source = notice_info.get('source')
            if source:
                status.source = source

        published_ts = entry_el.findtext('{http://www.w3.org/2005/Atom}published')
        published = iso8601.parse_date(published_ts).astimezone(iso8601.iso8601.Utc())
        status.created_at = published.replace(tzinfo=None)

        status.author = author
        status.save()

        # TODO: only UserStream the ones that a user has subscribed to?
        user = User.objects.get(pk=1)
        item, created = UserStream.objects.get_or_create(user=user, status=status,
            defaults={'display_at': status.created_at})

#django_push.subscriber.signals.updated_xml.connect(yo_hay)
django_push.subscriber.signals.updated_xml.connect(save_items)
