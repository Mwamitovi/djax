#!/usr/bin/python/
from django.contrib import admin
from .models import Entity, Location

admin.autodiscover()
admin.site.register(Entity)
admin.site.register(Location)
