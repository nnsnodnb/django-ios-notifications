from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from .models import DeviceToken

import json


def device_token_receive(request):
    if request.method != 'PUT':
        return HttpResponse(status=405)

    if request.body is b'':
        return JsonResponse({'error': 'Bad Request'}, status=400)

    query_dict = request.body.decode('utf-8')
    body = json.loads(query_dict)

    device_token = body['device_token']
    uuid = body['uuid']

    if DeviceToken.objects.filter(uuid=uuid).count() != 0:
        token = DeviceToken.objects.get(uuid=uuid)
        token.device_token = device_token
        token.save
    else:
        token = DeviceToken()
        token.device_token = device_token
        token.uuid = uuid
        token.save()

    return JsonResponse({'result': 'success'}, status=200)

