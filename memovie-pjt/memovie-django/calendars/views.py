from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Calendar
from .serializers import CalendarListSerializer, CalendarSerializer
from django.shortcuts import get_object_or_404, get_list_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def calendar_list(request):
    if request.method == 'GET':
        calendars = Calendar.objects.filter(user=request.user)  # 필터링
        serializer = CalendarListSerializer(calendars, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CalendarListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def calendar_detail(request, calendar_pk):
    calendar = get_object_or_404(Calendar, pk=calendar_pk)

    if request.method == 'GET':
        calendar.save()
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CalendarSerializer(calendar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)