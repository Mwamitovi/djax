#!/usr/bin/python/
from django.http import HttpResponse
import json


def ajax_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        output = json.dumps({'not_authenticated': True})
        return HttpResponse(output, mimetype='application/json')
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
