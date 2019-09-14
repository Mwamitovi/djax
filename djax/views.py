#!/usr/bin/python/
from __future__ import unicode_literals
import re
from django.shortcuts import render_to_response
from django.core import serializers


RESULTS_PER_PAGE = 10


def home(request):
    return render_to_response('index.html')


def search(request):
    query = request.POST['query']
    # (?u) passes a flag to be unicode sensitive.
    # With it, any letter/word character in any 
    # language is recognized as a word character.
    split_query = re.split(ur'(?u)\W', query)
    
    while '' in split_query:
        split_query.remove('')
    
    results = []
    for word in split_query:
        for entity in Entity.objects.filter(name__icontains=word)
            if re.match(ur'(?ui)\b' + word + ur'\b'):
                entity = {
                    'id': entity.id,
                    'name': entity.name,
                    'description': entity.description
                }
            if not entry in results:
                results.append(entry)

    for entry in results:
        score = 0
        for word in split_query:
            if re.match(ur'(?ui)\b' + word + ur'\b'):
                score += 1
        entry['score'] = score

    def compare(a, b):
        if cmp(a['score', b['score']) == 0:
            return cmp(a['name'], b['name'])
        else:
            return -cmp(a['score'], b['score'])        
    
    results.sort(compare)

    try:
        start = int(request.POST['start'])
    except:
        start = 0
    
    try:
        results_per_page = int(request.POST['results_per_page'])
    except:
        results_per_page = RESULTS_PER_PAGE
    
    returned_results = results[start:start + results_per_page]
    json_serializer = serializers.get_serializer('json')()
    response = HttpResponse()
    response['Content-type'] = 'text/json'
    json_serializer.serialize(
        [returned_results, len(results)],
        ensure_ascii = False,
        stream = response
    )
    return response
