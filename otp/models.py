from django.db import models
from users.models import PhoneNumber
import random

# Create your models here.


class Otp(models.Model):
    code = models.CharField(max_length=6, blank=True)
    phone_no = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.code = code_string
        super().save(*args, **kwargs)
