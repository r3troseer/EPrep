from django.db import models
from django.db.models import Q
import datetime

# Create your models here.

# def year_choice
levels = (('jss', 'jss'),
          ('sss', 'sss'),
          ('UTME','UTME'),
          ('IE','IE'),
          )
    
jss = (
    ('jss1','Junior Secondary School 1'),
    ('jss2','Junior Secondary School 2'),
    ('jss3','Junior Secondary School 3')
)

class jss(models.Model):
    classes = models.CharField(max_length=20, choices=jss)


class CourseQuerySet(models.QuerySet):
    def search(self,query):
        lookup = Q(name_icontains=query) | Q(body_icontains=query)
        qs = self.filter(lookup)
        return qs 

class level(models.Model):
    name = models.CharField(max_length=50, choices=levels)

    def __str__(self):
        return self.name


# class Class(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    body = models.TextField()

    def __str__(self):
        return self.name


# class Question(models.Model):
#     year = models.IntegerField(('Year'))

#     def __str__(self):
#         return self.year
