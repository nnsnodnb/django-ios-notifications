from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeviceToken
from .send import send_notification

import json


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


def send_notification_with_device_token(request, mode, device_token):
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
        send_notification(message=message,
                          device_token=device_token.device_token,
                          use_sandbox=True if int(mode) == 0 else False)
        return HttpResponse('Successful sending.', status=200)
    except:
        return HttpResponse('Not found. Your device token.', status=404)
