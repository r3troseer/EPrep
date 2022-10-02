from rest_framework.serializers import ModelSerializer
from .models import Otp


class OtpSerializer(ModelSerializer):
    class Meta:
        model = Otp
        fields = ('code')  