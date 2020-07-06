from django.forms import ModelForm,widgets

from appeal.models import AppealArticleModel


class AppealForm(ModelForm):

    class Meta:
        model = AppealArticleModel
        fields = ["appealed_article","appeal_options","appeal_body"]
        widgets = {
            "appealed_article":widgets.HiddenInput(),
            "appeal_options":widgets.RadioSelect()
        }