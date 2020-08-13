from django import forms


class IdForm(forms.Form):
    id = forms.CharField(label='id', max_length=20)
