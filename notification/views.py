from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .form import CertFileUploadForm
from .models import DeviceToken
from .send import send_notification

import json
import os
import threading

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


@csrf_exempt
def device_token_receive(request):
    if request.method != 'PUT':
        return HttpResponse(status=405)

    if request.body is b'':
        return JsonResponse({'error': 'Bad Request'}, status=400)

    query_dict = request.body.decode('utf-8')
    body = json.loads(query_dict)

    if 'device_token' not in body:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    if 'uuid' not in body:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    device_token = body['device_token']
    uuid = body['uuid']

    if DeviceToken.objects.filter(uuid=uuid).count() != 0:
        token = DeviceToken.objects.get(uuid=uuid)
        token.device_token = device_token
        token.save()
    else:
        token = DeviceToken()
        token.device_token = device_token
        token.uuid = uuid
        token.save()

    return JsonResponse({'result': 'success'}, status=200)


def send_notification_with_device_token(request, mode, device_token, execute=True):
    # mode: 0 or 1
    # 0: develop target
    # 1: product target

    if request.user is None or not request.user.is_superuser:
        return HttpResponse('Please login for admin user.', status=401)

    if int(mode) > 1:
        return HttpResponse('check your mode number(0 or 1).', status=400)

    message = 'This is test push notification.'
    if 'message' in request.GET:
        message = request.GET['message']

    try:
        device_token = DeviceToken.objects.get(device_token=device_token)
        if not execute:
            return HttpResponse('End process.', status=200)
        t = threading.Thread(target=send_notification, args=(message,
                                                             device_token.device_token,
                                                             True if int(mode) == 0 else False))
        t.start()
        return HttpResponse('Successful sending.', status=200)
    except:
        return HttpResponse('Not found. Your device token.', status=404)


def cert_upload(request):
    if not request.user.is_superuser:
        return HttpResponse('Access Denied', status=403)

    if request.method == 'POST':
        form = CertFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cert_file = request.FILES['file']
            if not cert_file.name.endswith('.p12'):
                return render(request, 'upload.html', {'error': 'wrong'})

            destination = open(UPLOAD_DIR + cert_file.name, 'wb+')
            for chunk in cert_file.chunks():
                destination.write(chunk)
            destination.close()
            return render(request, 'upload.html', {'error': None})
        else:
            return render(request, 'upload.html', {'error': 'invalid'})
    else:
        form = CertFileUploadForm()
        return render(request, 'upload.html', {'form': form})
