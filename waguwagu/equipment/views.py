from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render, redirect
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework.parsers import JSONParser
from decimal import Decimal, InvalidOperation


class RestaurantListAPI(APIView):
    parser_classes = [JSONParser]  # JSON 요청 파싱

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     data = request.data.copy()

    #     # 안전하게 변환
    #     try:
    #         if 'price' in data:
    #             data['price'] = str(Decimal(data['price']))
    #     except (InvalidOperation, TypeError, ValueError):
    #         return Response({"price": ["유효한 숫자를 입력하세요."]}, status=400)

    #     for field in ['latitude', 'longitude']:
    #         try:
    #             if field in data and data[field] not in [None, '']:
    #                 data[field] = float(data[field])
    #             else:
    #                 data[field] = None
    #         except ValueError:
    #             return Response({field: ["유효한 좌표를 입력하세요."]}, status=400)

    #     serializer = RestaurantSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        print("===== POST DATA =====")
        print(request.data)  # 실제 클라이언트에서 받은 JSON
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print("===== SERIALIZER ERRORS =====")
        print(serializer.errors)
        return Response(serializer.errors, status=400)



class RestaurantDetailAPI(APIView):
    parser_classes = [JSONParser]

    def get(self, request, id):
        restaurant = get_object_or_404(Restaurant, id=id)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)
    
    def put(self, request, id):
        restaurant = get_object_or_404(Restaurant, id=id)
        data = request.data.copy()

        # 안전하게 변환
        try:
            if 'price' in data:
                data['price'] = str(Decimal(data['price']))
        except (InvalidOperation, TypeError, ValueError):
            return Response({"price": ["유효한 숫자를 입력하세요."]}, status=400)

        for field in ['latitude', 'longitude']:
            try:
                if field in data and data[field] not in [None, '']:
                    data[field] = float(data[field])
                else:
                    data[field] = None
            except ValueError:
                return Response({field: ["유효한 좌표를 입력하세요."]}, status=400)

        serializer = RestaurantSerializer(restaurant, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        restaurant = get_object_or_404(Restaurant, id=id)
        restaurant.delete()
        return Response(status=204)


# 저장된 레스토랑 목록 화면
def saved_restaurants_view(request):
    restaurants = Restaurant.objects.all().order_by('-created_at')
    return render(request, "equipment/saved.html", {"restaurants": restaurants})


# HTML form POST 처리용 view
def save_restaurant(request):
    if request.method == "POST":
        name = request.POST.get("name")
        menu = request.POST.get("menu")
        price = request.POST.get("price")
        location = request.POST.get("location")
        memo = request.POST.get("memo")
        latitude = request.POST.get("latitude") or None
        longitude = request.POST.get("longitude") or None

        try:
            price = str(Decimal(price))
        except (InvalidOperation, TypeError, ValueError):
            return redirect("/map/")  # 잘못된 가격 입력 시 지도 화면으로

        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except ValueError:
            latitude = None
            longitude = None

        if name and menu and price and location and memo:
            Restaurant.objects.create(
                name=name,
                menu=menu,
                price=price,
                location=location,
                memo=memo,
                latitude=latitude,
                longitude=longitude
            )
        return redirect("/saved/")
    return redirect("/map/")
