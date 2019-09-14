#!/usr/bin/python
import re
import datetime
from django.db import models
from tagging.registry import register


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

    
class TextEmailField(models.EmailField):
    entity = models.ForiegnKey('Entity')

    def get_internal_type(self):
        return u'TextField'


class TextURLField(models.URLField):
    def get_internal_type(self):
        return u'TextField'


class TextPhoneField(models.TextField):
    number = TextField()
    description = TextField()

    def __eq__(self, other):
        try:
            return self.remove_formatting() == other.remove_formatting()
        except:
            return False
    
    def remove_formatting(self):
        return re.sub(ur'\D', u'', str(self)


class Entity(models.Model):
    """
    This class is basically the "Person" class; 
    however, it is called "Entity" to emphasize that 
    it is intended to accommodate people, offices, organizational units, 
    and possibly other areas.
    """
    active = models.BooleanField(required=False)
    department = models.ForeignKey(Entity, required=False)
    description = models.TextField(required=False)
    email = TextEmailField(required=False)
    extension = ExtensionField(required=False)
    homepage = TextURLField(required=False)
    image = models.FileField(required=False)
    location = LocationField(required=False)
    honors = models.TextField(required=False)
    name = models.TextField()
    post_nominals = models.TextField(required=False)
    publish_externally = models.BooleanField(required=False)
    reports_to = models.ForeignKey(Entity, required=False)
    start_date = models.DateField(required=False)


# register Entity model to use with the tagging application
# tagging is intended atleast initially to locate areas of expertise
register(Entity)
