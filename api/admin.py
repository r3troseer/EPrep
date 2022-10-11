from django.contrib import admin
from .models import Course, Lesson, Level, SubLevel, Class, Department, Exam, UTME


# admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Level)
admin.site.register(SubLevel)
admin.site.register(Class)
admin.site.register(Department)
admin.site.register(Exam)
admin.site.register(UTME)
