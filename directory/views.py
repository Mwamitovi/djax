# !/usr/bin/python/
from __future__ import unicode_literals
import re
import json
from functools import cmp_to_key

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate, login
from .models import Entity
from .functions import ajax_login_required

RESULTS_PER_PAGE = 10


def ajax_login_request(request):
    """
    We check for key in request.POST,
    if non-existent, we default to a request.GET
    """
    try:
        request.POST['login']
        dictionary = request.POST
    except KeyError:
        dictionary = request.GET

    user = authenticate(
        username=dictionary['login'],
        password=dictionary['password']
    )

    if user and user.is_active:
        login(request, user)
        result = True
    else:
        result = False

    return HttpResponse(json.dumps(result), mimetype='application/json')


def home(request):
    return render(request, 'search.html')


@ajax_login_required
def search(request):
    try:
        query = request.POST['query']
        dictionary = request.POST
    except KeyError:
        query = request.GET['query']
        dictionary = request.GET

    # (?u) passes a flag to be unicode sensitive.
    # With it, any letter/word character in any
    # language is recognized as a word character.
    split_query = re.split(r'(?u)\W', query)

    while '' in split_query:
        split_query.remove('')

    results = []
    for word in split_query:
        for entity in Entity.objects.filter(name__icontains=word):
            # ignore case, and do unicode matching
            if re.match(r'(?ui)\b' + word + r'\b'):
                entry = {
                    'id': entity.id,
                    'name': entity.name,
                    'description': entity.description
                }
            if entry not in results:
                results.append(entry)

    for entry in results:
        score = 0
        for word in split_query:
            if re.match(r'(?ui)\b' + word + r'\b'):
                score += 1
        entry['score'] = score

    def compare(a, b):
        x = a['score']
        y = b['score']
        # python3 work around for the removed cmp()
        if ((x > y) - (x < y)) == 0:
            return (x > y) - (x < y)
        else:
            return -((x > y) - (x < y))

    results.sort(key=cmp_to_key(compare))

    try:
        start = int(dictionary['start'])
    except KeyError:
        start = 0

    try:
        results_per_page = int(dictionary['results_per_page'])
    except KeyError:
        results_per_page = RESULTS_PER_PAGE

    returned_results = results[start:start + results_per_page]
    response = HttpResponse(
        json.dumps([returned_results, len(results)]),
        mimetype='application/json'
    )
    return response
