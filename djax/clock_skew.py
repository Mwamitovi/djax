#!/usr/bin/python/
import json
import time
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response


def home(request):
    return render_to_response('closure/clockskew.html')


def timestamp(request):
    return HttpResponse(
        json.dumps({'time': 1000*time.time()}),
        content_type='application/json'
    )
