# !/usr/bin/python/
from __future__ import unicode_literals
import re
from functools import cmp_to_key

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Entity

RESULTS_PER_PAGE = 10


def home(request):
    return render(request, 'index.html')


def search(request):
    query = request.POST['query']
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
        start = int(request.POST['start'])
    except KeyError:
        start = 0

    try:
        results_per_page = int(request.POST['results_per_page'])
    except KeyError:
        results_per_page = RESULTS_PER_PAGE

    returned_results = results[start:start + results_per_page]
    json_serializer = serializers.get_serializer('json')()
    response = HttpResponse()
    response['Content-type'] = 'text/json'
    json_serializer.serialize(
        [returned_results, len(results)],
        ensure_ascii=False,
        stream=response
    )
    return response
