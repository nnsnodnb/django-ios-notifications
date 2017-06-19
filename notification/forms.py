from django import forms


class CertFileUploadForm(forms.Form):
    cert_file = forms.FileField()
    target = forms.ChoiceField(choices=((0, 'Develop'), (1, 'Distribute')), required=True, widget=forms.RadioSelect)


class NotificationSendForm(forms.Form):
    target = forms.ChoiceField(choices=((0, 'Develop'), (1, 'Distribute')),
                               widget=forms.RadioSelect,
                               initial=0,
                               required=True)
    title = forms.CharField(required=True)
    subtitle = forms.CharField(required=False)
    body = forms.CharField(required=False)
    sound = forms.CharField(initial='default', required=True)
    badge = forms.IntegerField(initial=1, min_value=0, required=True)
    content_available = forms.BooleanField(initial=False, required=False)
    mutable_content = forms.BooleanField(initial=False, required=False)
    extra = forms.CharField(widget=forms.Textarea, required=False)
