from django.db import models
from django.db.models import Q
import datetime

# Create your models here.

# def level_choices
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


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=100, choices=levels)

    def __str__(self):
        return self.name


class SubLevel(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Class(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(Course)

    # def __str__(self):
    #     return self.subject


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


class UTME(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name='lesson', null=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    note = models.CharField(max_length=500)
    videoUrl = models.CharField(max_length=1500, null=True)
    thumbnailUrl = models.CharField(max_length=1500, null=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, related_name='topic', null=True)

    def __str__(self):
        return self.note

# class Question(models.Model):
#     year = models.IntegerField(('Year'))

#     def __str__(self):
#         return self.year
