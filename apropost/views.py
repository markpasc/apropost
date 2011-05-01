from django.conf import settings
import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth.views
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from apropost.models import UserStream, Author
from apropost.forms import UserCreationForm


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

            Author.objects.create(
                user=user,
                screen_name=user.username,
                display_name=user.username,
                atom_id='http://%s.%s/' % (user.username, root_site.domain),
            )

            django.contrib.auth.login(request, user)
            return HttpResponseRedirect(new_url)
    else:
        form = UserCreationForm()

    data = {'form': form}
    return render(request, 'apropost/register.html', data)


@login_required
def home(request):
    stream = UserStream.objects.filter(user=request.user).order_by('-display_at').select_related()

    user_authors = request.user.author_set.all()
    try:
        author = user_authors[0]
    except IndexError:
        # TODO: should switch to a flow for making an Author for the user?
        raise

    data = {
        'author': author,
        'stream': stream[:20],
    }

    return render(request, 'apropost/home.html', data)
