from django import forms
from django.forms import widgets


class EmailCheckForm(forms.Form):
    email = forms.EmailField(required=True)
    oauthid = forms.IntegerField(required=True)
    def __init__(self,*args,**kwargs):
        super(EmailCheckForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget = widgets.EmailInput(
            attrs={"placeholder":"请输入邮箱","class":"form-control","height":"50px"}
        )