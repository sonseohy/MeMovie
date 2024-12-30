from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentListSerializer, CommentSerializer

from django.shortcuts import get_object_or_404, get_list_or_404

# 전체 게시글 조회 및 게시글 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.user is None:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 로그인한 사용자를 author로 설정
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 상세 게시글 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 게시글 조회 (GET)
    if request.method == 'GET':
        # 조회수 증가
        article.article_views += 1
        article.save()  # 조회수 증가 후 저장
        
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)
    
    # 게시글 수정 (PUT)
    elif request.method == 'PUT':
        print(article.author, request.user)
        if article.author  != request.user:
            return Response({"detail": "You do not have permission to edit this article."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(article, data=request.data, partial=True)  # partial=True -> 일부 수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제 (DELETE)
    elif request.method == 'DELETE':
        if article.author != request.user:
            return Response({"detail": "You do not have permission to delete this article."},
                            status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comment(request, article_pk):
    # article_pk에 해당하는 Article 객체를 가져옵니다. 존재하지 않으면 404 오류 발생
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'GET':
        # GET 요청일 경우, 해당 article에 속한 모든 댓글을 가져옵니다.
        comments = article.comment_set.all()
        # 댓글을 직렬화합니다.
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # POST 요청일 경우, 새로운 댓글을 생성합니다.
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # 댓글을 저장하고, article과 user를 연결합니다.
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 좋아요 토글 처리
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    
    # 응답 반환: 좋아요 여부와 좋아요 사용자 수
    return Response({
        'is_liked': is_liked,
        'like_users_count': article.like_users.count(),
    }, status=status.HTTP_200_OK)