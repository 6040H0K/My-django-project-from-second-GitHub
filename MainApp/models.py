from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class School(models.Model):
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    town = models.CharField(max_length=255)
    clases = models.JSONField()
    lessons = models.JSONField()
    class_form = models.JSONField()
    lesson_form = models.JSONField()
    password = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add = True)
    time_update = models.DateTimeField(auto_now= True)
    

# class SchoolClass(models.Model):
#     title = models.CharField(max_length=255)
#     rank = models.IntegerField()
#     schedule = models.JSONField()
#     studensts = models.JSONField()
#     lessons = models.JSONField
#     time_create = models.DateTimeField(auto_now_add = True)
#     time_update = models.DateTimeField(auto_now= True)