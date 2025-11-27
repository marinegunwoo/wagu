from django.urls import path
from equipment.views import (
    RestaurantListAPI,
    RestaurantDetailAPI,
    saved_restaurants_view
)
from django.http import HttpResponse
from django.views.generic import TemplateView

def home(request):
    return HttpResponse("맛집 API 홈: /map/ 로 접근하세요")

urlpatterns = [
    path('', home),
    # Map 화면
    path('map/', TemplateView.as_view(template_name='equipment/map.html')),
    # REST API 엔드포인트
    path('restaurants/', RestaurantListAPI.as_view(), name='restaurant-list'),
    # 개별 맛집 상세
    path('restaurants/<int:id>/', RestaurantDetailAPI.as_view(), name='restaurant-detail'),
    # 저장된 데이터 보기
    path('saved/', saved_restaurants_view, name="saved-restaurants"),
]
