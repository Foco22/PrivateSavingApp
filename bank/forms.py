from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=1000)
    saving_target = forms.CharField(label='saving_target', max_length=1000)
    link_token = forms.CharField(label='link_token', max_length=10000)
    security_token = forms.CharField(label='security_token', max_length=10000)


