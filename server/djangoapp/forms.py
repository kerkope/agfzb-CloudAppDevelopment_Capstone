from django import forms
  
# creating a form
class OptionalPersonForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    user_name = forms.CharField(required=True)
    password = forms.CharField(widget = forms.PasswordInput())