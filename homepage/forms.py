from django import forms

class HandleForm(forms.Form):
    handle = forms.CharField(label='Enter Handle', max_length=100)