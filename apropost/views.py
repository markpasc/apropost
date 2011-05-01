from django.conf import settings
import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth.views
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_push.subscriber.models import Subscription
import feedparser

from apropost.models import UserStream, Author, AuthorSubscription
from apropost.forms import UserCreationForm, AddSubscriptionForm


def root(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    return django.contrib.auth.views.login(request, template_name='apropost/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            root_site = Site.objects.get(pk=settings.SITE_ID)
            userdomain = '%s.%s' % (user.username, root_site.domain)
            new_url = 'http://%s%s' % (userdomain, reverse('home'))

            django.contrib.auth.login(request, user)
            return HttpResponseRedirect(new_url)
    else:
        form = UserCreationForm()

    data = {'form': form}
    return render(request, 'apropost/register.html', data)


@login_required
def home(request):
    stream = UserStream.objects.filter(user=request.user).order_by('-display_at').select_related()

    data = {
        'stream': stream[:20],
    }

    return render(request, 'apropost/home.html', data)


@login_required
def add_subscription(request):
    if request.method == 'POST':
        form = AddSubscriptionForm(request.POST)
        if form.is_valid():

            url = form.cleaned_data['url']
            # Is this a feed or a web page with a feed?

            feed_url = url
            buh = feedparser.parse(feed_url)
            if buh.bozo and buh['headers']['content-type'].startswith('text/html'):
                feedlinks = [l['href'] for l in buh.feed.links if l['rel'] == 'alternate' and l['type'] in ('application/atom+xml', 'application/rss+xml')]
                if feedlinks:
                    feed_url = feedlinks[0]
                    buh = feedparser.parse(feed_url)

            hublinks = [l['href'] for l in buh.feed.links if l['rel'] == 'hub']
            if hublinks:
                hub_url = hublinks[0]
            else:
                raise ValueError("No such hub for %s :(" % feed_url)

            sub = Subscription.objects.subscribe(feed_url, hub=hub_url)
            author = Author.objects.create(
                atom_id=url,
                display_name=buh.feed.title,
                homepage_url=url,
            )
            AuthorSubscription.objects.create(author=author, subscription=sub)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = AddSubscriptionForm()

    data = {'form': form}
    return render(request, 'apropost/subscribe.html', data)
