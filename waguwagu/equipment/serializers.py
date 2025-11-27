from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    memo = serializers.CharField(required=True, allow_blank=True)  # 빈 문자열도 허용

    class Meta:
        model = Restaurant
        fields = '__all__'
