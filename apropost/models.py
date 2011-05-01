from datetime import datetime
from functools import wraps
from urlparse import urljoin
from xml.etree import ElementTree

from django.contrib.auth.models import User
from django.db import models
import django_push.subscriber.signals
from django_push.subscriber.models import Subscription
import iso8601


class Author(models.Model):

    atom_id = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    homepage_url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    #profile_image_url = ...
    #lang = ...
    #profile_design = ...
    #utc_offset = ...
    #time_zone = ...

    def __unicode__(self):
        return u'%s (%s)' % (self.screen_name, self.display_name)

    @classmethod
    def from_element(cls, author_el):
        # TODO: support data-only authors?
        author_id = author_el.findtext('{http://www.w3.org/2005/Atom}uri')
        if author_id is None:
            return
        try:
            author = cls.objects.get(atom_id=author_id)
        except Author.DoesNotExist:
            author = cls(atom_id=author_id)

        # Fill in with Portable Contacts types.
        author.screen_name = author_el.findtext('{http://portablecontacts.net/spec/1.0}preferredUsername')
        author.display_name = author_el.findtext('{http://portablecontacts.net/spec/1.0}displayName')
        #author.description = ...?
        author.location = author_el.findtext('{http://portablecontacts.net/spec/1.0}address/{http://portablecontacts.net/spec/1.0}formatted')
        # ugh homepage url
        for url_el in author_el.findall('{http://portablecontacts.net/spec/1.0}urls'):
            if url_el.findtext('{http://portablecontacts.net/spec/1.0}type') in ('home', 'homepage') and url_el.findtext('{http://portablecontacts.net/spec/1.0}primary') == 'true':
                author.homepage_url = url_el.findtext('{http://portablecontacts.net/spec/1.0}value')

        author.save()
        return author


class AuthorSubscription(models.Model):

    author = models.ForeignKey(Author)
    subscription = models.ForeignKey(Subscription, unique=True)


class Image(models.Model):

    image_url = models.CharField(max_length=200, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()


class Post(models.Model):

    atom_id = models.CharField(max_length=200)
    author = models.ForeignKey(Author, blank=True, null=True)
    avatar = models.ForeignKey(Image, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    source = models.CharField(max_length=200, blank=True)

    created = models.DateTimeField(default=datetime.now)
    published = models.DateTimeField(default=datetime.now)

    in_reply_to = models.ForeignKey('Post', blank=True, null=True, related_name='replies')
    conversation = models.ForeignKey('Post', blank=True, null=True, related_name='conversation_replies')

    RENDER_MODE_CHOICES = (
        ('mixed', 'mixed'),
        ('status', 'status'),
        ('image', 'image'),
        ('link', 'link'),
    )
    render_mode = models.CharField(max_length=15, blank=True, default='mixed', choices=RENDER_MODE_CHOICES)
    #image = models.ForeignKey(Image, null=True, blank=True, related_name="represented_objects")
    permalink_url = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u'%s: "%s"' % (self.author.screen_name, self.text[:100])

    @classmethod
    def from_element(cls, entry_el, feed_author_el=None):
        object_type = entry_el.findtext('{http://activitystrea.ms/spec/1.0/}object-type')
        if object_type is not None:
            object_type = urljoin('http://activitystrea.ms/schema/1.0/', object_type)
        # TODO: support bookmarks and photos
        if object_type not in (None, 'http://activitystrea.ms/schema/1.0/note', 'http://activitystrea.ms/schema/1.0/post'):
            return

        verb = entry_el.findtext('{http://activitystrea.ms/spec/1.0/}verb')
        if verb is None:
            verb = 'post'
        verb = urljoin('http://activitystrea.ms/schema/1.0/', verb)
        # TODO: support like/favorite and share
        if verb != 'http://activitystrea.ms/schema/1.0/post':
            return

        atom_id = entry_el.findtext('{http://www.w3.org/2005/Atom}id')
        if atom_id is None:
            # IDs are table stakes.
            return
        try:
            post = cls.objects.get(atom_id=atom_id)
            # TODO: We're really updating this item. Is this publisher authoritative for this atom id?
        except Post.DoesNotExist:
            post = cls(atom_id=atom_id)

        # TODO: try content first if there ever is one
        content = entry_el.find('{http://www.w3.org/2005/Atom}content')
        content_type = content.get('type', 'html')
        if content_type == 'html':
            post.text = content.text
        else:
            raise ValueError("Unsupported content element type %r" % content_type)

        notice_info = entry_el.find('{http://status.net/schema/api/1/}notice_info')
        if notice_info is not None:
            source = notice_info.get('source')
            if source:
                post.source = source

        published_ts = entry_el.findtext('{http://www.w3.org/2005/Atom}published')
        published = iso8601.parse_date(published_ts).astimezone(iso8601.iso8601.Utc())
        post.published = published.replace(tzinfo=None, microseconds=0)

        author_el = entry_el.find('./{http://www.w3.org/2005/Atom}author')
        if author_el is None:
            author_el = feed_author_el
        if author_el is not None:
            post.author = Author.from_element(author_el)

        post.save()
        return post


class StreamWhy(models.Model):

    actor = models.ForeignKey(Author)
    verb = models.CharField(max_length=100)


class UserStream(models.Model):

    user = models.ForeignKey('auth.User')
    post = models.ForeignKey(Post)
    display_at = models.DateTimeField()
    why = models.ForeignKey(StreamWhy, blank=True, null=True)

    def __unicode__(self):
        return u'%r for %s at %s' % (self.post, self.user.username, self.display_at.isoformat(' '))


def oops(fn):
    @wraps(fn)
    def hoops(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception, exc:
            logging.exception(exc)
    return hoops

def yo_hay(notification, **kwargs):
    import logging
    xml = ElementTree.tostring(notification, encoding='utf-8')
    logging.getLogger(__name__).debug(xml)

def save_items(notification, **kwargs):
    feed_author_el = notification.find('./{http://www.w3.org/2005/Atom}author')
    if feed_author_el is None:
        sender = kwargs['sender']
        assert isinstance(sender, Subscription)
        feed_author = AuthorSubscription.objects.get(subscription=sender).author
    else:
        feed_author = Author.from_element(feed_author_el)

    for entry_el in notification.findall('{http://www.w3.org/2005/Atom}entry'):
        post = Post.from_element(entry_el, feed_author=feed_author)
        post.save()

        # TODO: only UserStream the ones that a user has subscribed to?
        user = User.objects.get(pk=1)
        item, created = UserStream.objects.get_or_create(user=user, post=post,
            defaults={'display_at': post.created_at})

django_push.subscriber.signals.updated_xml.connect(yo_hay)
django_push.subscriber.signals.updated_xml.connect(oops(save_items))
