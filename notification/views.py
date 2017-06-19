from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import CertFileUploadForm, NotificationSendForm
from .models import DeviceToken
from .utils import send_notification, upload_certificate

import json


@csrf_exempt
@require_http_methods(['PUT'])
def device_token_receive(request):
    if request.body is b'':
        return JsonResponse({'error': 'Bad Request'}, status=400)

    query_dict = request.body.decode('utf-8')
    body = json.loads(query_dict)

    error = False
    if 'device_token' not in body:
        error = True
    if 'uuid' not in body:
        error = True
    if 'sandbox' not in body:
        error = True

    if error:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    device_token = body['device_token']
    uuid = body['uuid']
    sandbox = body['sandbox']

    if DeviceToken.objects.filter(uuid=uuid).count() != 0:
        token = DeviceToken.objects.get(uuid=uuid)
        token.device_token = device_token
        token.use_sandbox = sandbox
        token.save()
    else:
        token = DeviceToken()
        token.device_token = device_token
        token.uuid = uuid
        token.use_sandbox = sandbox
        token.save()

    return JsonResponse({'result': 'success'}, status=200)


@login_required(login_url='/login')
@require_http_methods(['GET'])
@user_passes_test(lambda user: user.is_superuser)
def send_notification_with_device_token(request, mode, device_token, execute=True):
    # mode: 0 or 1
    # 0: develop target
    # 1: product target

    if int(mode) > 1:
        return HttpResponse('check your mode number(0 or 1).', status=400)

    message = 'This is test push notification.'
    if 'message' in request.GET:
        message = request.GET['message']

    try:
        device_token = DeviceToken.objects.get(device_token=device_token)
        if not execute:
            return HttpResponse('End process.', status=200)

        send_notification(message=message,
                          device_token=device_token.device_token,
                          use_sandbox=True if int(mode) == 0 else False)
        return HttpResponse('Successful sending.', status=200)
    except:
        return HttpResponse('Not found. Your device token.', status=404)


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda user: user.is_superuser)
def cert_upload(request):
    if request.method == 'POST':
        form = CertFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = upload_certificate(request.FILES['cert_file'], target_mode=int(request.POST['target']))
            return render(request, 'upload.html', result)

        else:
            return render(request, 'upload.html', {'error': 'invalid'}, status=400)
    else:
        form = CertFileUploadForm()
        return render(request, 'upload.html', {'form': form})


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda user: user.is_superuser)
def send_notification_form(request):
    if request.method == 'POST':
        form = NotificationSendForm(request.POST)
        if form.is_valid():
            target = request.POST['target']
            device_tokens = list(map(lambda token_id: DeviceToken.objects.get(id=token_id).device_token,
                                     request.POST.getlist('device_token')))
            title = request.POST['title']
            subtitle = request.POST['subtitle'] or None
            body = request.POST['body'] or None
            sound = request.POST['sound']
            badge = int(request.POST['badge'])
            content_available = True if 'content_available' in request.POST else False
            mutable_content = True if 'mutable_content' in request.POST else False
            extra = request.POST['extra'] or None
            return redirect('notification:send_form')

        else:
            return redirect('notification:send_form')

    else:
        form = NotificationSendForm()
        target = 0
        use_sandbox = True

        if 'target' in request.GET:
            target = int(request.GET['target'])
            use_sandbox = not target

        form.fields['target'].initial = target
        device_tokens = DeviceToken.objects.filter(use_sandbox=use_sandbox)
        if device_tokens.count() == 0:
            form.fields['device_token'].widget = forms.HiddenInput()
        form.fields['device_token'].choices = lambda: ((token.id, token.device_token) for token in device_tokens)
        return render(request, 'send_form.html', {'form': form})
