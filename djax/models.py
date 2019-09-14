#!/usr/bin/python
from django.db import models
import datetime


OFFICE_CHOICES = (
    (u'KLA', u'Kampala Office, Central, Uganda'),
    (u'MKN', u'Busia Office, Eastern, Uganda'),
    (u'WAK', u'Gulu Office, Northern, Uganda'),
    (u'MSK', u'Hoima Office, Western, Uganda'),
    (u'KAB', u'Kabale Office, South-Western Uganda'),
)


class Location(models.Model):
    notes = models.TextField(required=False)
    office = models.CharField(max_length=2, choices=OFFICE_CHOICES, required=False)
    postal_address = models.TextField(required=False)
    room = models.TextField(required=False)
    coordinates = GPSCoordinate(required=False)

    

