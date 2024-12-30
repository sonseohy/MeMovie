from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from .serializers import UserUpdateSerializer, UserProfileSerializer
import uuid

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from movies.models import Genre

# profile 뷰에서 genres 배열 처리
@api_view(["GET", "POST", "PUT"])
def profile(request, username):
    try:
        person = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # GET 요청 처리: 사용자의 프로필 정보 반환
    if request.method == "GET":
        serializer = UserProfileSerializer(person)
        return Response(serializer.data, status=200)

    # PUT 요청 처리: 프로필 정보 업데이트
    elif request.method == "PUT":
        serializer = UserUpdateSerializer(person, data=request.data, partial=True)

        if serializer.is_valid():
            person = serializer.save()  # 장르 포함 모든 데이터 저장
            serializer = UserProfileSerializer(person)  # 업데이트된 데이터 반환
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


    # POST 요청 처리: 프로필 이미지 업로드
    elif request.method == "POST":
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            # UUID 기반으로 파일명 변경하여 저장 (충돌 방지)
            file_name = f"{uuid.uuid4().hex}_{profile_image.name}"
            file_path = default_storage.save(f'profile_images/{file_name}', profile_image)

            # 저장된 파일의 URL 생성
            file_url = default_storage.url(file_path)

            # 사용자 모델에 프로필 이미지 URL 저장
            person.profile_picture = file_url
            person.save()

            # 성공적으로 이미지 업로드 후 응답
            return Response({'image_url': file_url}, status=200)

        else:
            return Response({'error': 'No profile image provided'}, status=400)

# 수정 필요
@api_view(["POST"])
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)

    if request.user != you:
        if request.user in you.followers.all():
            you.followers.remove(request.user)
        else:
            you.followers.add(request.user)
        return redirect('accounts:profile', you.username)
    