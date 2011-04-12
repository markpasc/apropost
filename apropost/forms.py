import django.contrib.auth.forms
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):

    username = forms.RegexField(label=_("Screen name"), max_length=30,
        regex=r'^[a-z0-9](?:[-a-z0-9]*[a-z0-9])?$',
        error_messages={
            'invalid': _("This value may contain only letters and numbers (and '-' characters, if they're in the middle)."),
        })
