from django import forms


class CertFileUploadForm(forms.Form):
    cert_file = forms.FileField()
    target = forms.ChoiceField(choices=((0, 'Develop'), (1, 'Distribute')), required=True, widget=forms.RadioSelect)
