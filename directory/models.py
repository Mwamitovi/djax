# !/usr/bin/python
from __future__ import unicode_literals
import re
from datetime import datetime
from django.db import models
from tagging.registry import register

OFFICE_CHOICES = (
    ('KLA', 'Kampala Office, Central, Uganda'),
    ('MKN', 'Busia Office, Eastern, Uganda'),
    ('WAK', 'Gulu Office, Northern, Uganda'),
    ('MSK', 'Hoima Office, Western, Uganda'),
    ('KAB', 'Kabale Office, South-Western Uganda'),
)


class Location(models.Model):
    notes = models.TextField(blank=True)
    office = models.CharField(max_length=2, choices=OFFICE_CHOICES, blank=True)
    postal_address = models.TextField(blank=True)
    room = models.TextField(blank=True)


class TextEmailField(models.EmailField):
    entity = models.ForeignKey('Entity')

    def get_internal_type(self):
        return 'TextField'


class TextURLField(models.URLField):
    def get_internal_type(self):
        return 'TextField'


class TextPhoneField(models.TextField):
    number = models.TextField()
    description = models.TextField()

    def __eq__(self, other):
        try:
            return self.remove_formatting() == other.remove_formatting()
        except ValueError:
            return False

    def remove_formatting(self):
        return re.sub(r'\D', '', str(self))


class Entity(models.Model):
    """
    This class is basically the "Person" class;
    however, it is called "Entity" to emphasize that
    it is intended to accommodate people, offices, organizational units,
    and possibly other areas.
    """
    active = models.BooleanField(blank=True)
    description = models.TextField()
    email = TextEmailField(blank=True)
    homepage = TextURLField(blank=True)
    image = models.FileField(blank=True)
    location = models.ForeignKey(Location, blank=True)
    honors = models.TextField()
    name = models.TextField()
    post_nominals = models.TextField()
    publish_externally = models.BooleanField(blank=True)
    start_date = models.DateField(blank=True)


# register Entity model to use with the tagging application
# tagging is intended at least initially to locate areas of expertise
register(Entity)


class TextStatus(models.Model):
    datetime = models.DateTimeField(default=datetime.now())
    entity = models.ForeignKey(Entity)
    text = models.TextField()
