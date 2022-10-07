from django.db import models
from django.db.models import Q
import datetime

# Create your models here.

# def year_choice
levels = (('JSS', 'Junior Secondary School'),
          ('SSS', 'Senior Secondary School'),
          ('UTME', 'UTME/PUTME'),
          ('IE', 'International Exams'),
          )


class CourseQuerySet(models.QuerySet):
    def search(self, query):
        lookup = Q(name_icontains=query) | Q(body_icontains=query)
        qs = self.filter(lookup)
        return qs


class Level(models.Model):
    name = models.CharField(max_length=100, choices=levels)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    body = models.TextField()

    def __str__(self):
        return self.name


# class Question(models.Model):
#     year = models.IntegerField(('Year'))

#     def __str__(self):
#         return self.year
