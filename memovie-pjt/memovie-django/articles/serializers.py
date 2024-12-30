from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model


# 작성자 정보 시리얼라이저
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'profile_picture')  # User 모델에서 닉네임과 프로필 이미지를 반환


# 게시글 목록을 위한 시리얼라이저 (읽기 전용, 제목과 작성자만 표시)
class ArticleListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # 작성자 정보 포함
    created_at = serializers.DateTimeField(format='%Y-%m-%d')  # 날짜만 출력

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'article_views', 'created_at', 'author', 'like_users')  # content 제외


# 게시글 상세 정보를 위한 시리얼라이저
class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # 작성자 정보 포함
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)  # 추천 수 추가
    is_liked = serializers.SerializerMethodField()  # 현재 사용자의 좋아요 상태

    class Meta:
        model = Article
        fields = '__all__'  # 모든 필드를 포함하되 content는 write_only로 설정하여 조회 시 포함하지 않음

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False


# 댓글 목록을 위한 시리얼라이저 (사용자 및 글 정보 포함)
class CommentListSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer(read_only=True)  # 게시글 정보 포함
    user = AuthorSerializer(read_only=True)  # 댓글 작성자 정보도 포함시킬 수 있음 (추가 구현 필요)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'article', 'created_at', 'updated_at')
        read_only_fields = ('article',)  # article은 작성 시에만 지정


# 댓글을 위한 시리얼라이저 (댓글 작성 및 조회 시 사용)
class CommentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)  # 댓글에 해당하는 게시글 정보 반환
    user = AuthorSerializer(read_only=True)  # 댓글 작성자 정보 포함

    class Meta:
        model = Comment
        fields = ('id', 'content', 'article', 'user', 'created_at', 'updated_at')
        read_only_fields = ('article', 'user', 'created_at', 'updated_at')  # 수정 불가 필드 설정
