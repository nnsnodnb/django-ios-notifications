from django import forms


class CertFileUploadForm(forms.Form):
    cert_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    cert_file = forms.FileField()
