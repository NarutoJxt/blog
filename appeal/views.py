from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView
from notifications.signals import notify

from appeal.forms import AppealForm


class AppealView(FormView):
    template_name = ""
    form_class = AppealForm
    def form_valid(self, form):
        appeal = form.save()
        appeal.save()
        url = appeal.appealed_article.get_absolute_url()
        notify.send(
            self.request.user,
            recipient=appeal.appealed_article.author,
            verb="投诉了你",
            target=appeal.appealed_article,
            action_object=appeal,
            description="appeal"
        )
        return HttpResponseRedirect(url)
