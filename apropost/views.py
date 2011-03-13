from django.contrib.auth.decorators import login_required
import django.contrib.auth.views
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from apropost.models import UserStream


def root(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    return django.contrib.auth.views.login(request)


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
