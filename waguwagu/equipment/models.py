from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)  # 맛집 이름
    menu = models.CharField(max_length=200)  # 메뉴
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 가격
    location = models.CharField(max_length=200)  # 위치
    memo = models.CharField(max_length=300)  # 사용자 메모
    latitude = models.FloatField(null=True, blank=True)   # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
