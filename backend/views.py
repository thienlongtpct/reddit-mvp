# Create your views here.
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from backend.models import Post, Comment
import json
from backend.serializers import PostSerializer, CommentSerializer
import redis
from config import *

r = redis.Redis(host=mysql_host, port=mysql_port, db=0, charset="utf-8", decode_responses=True)


class TestView(GenericAPIView):
    authentication_classes = ()

    """
    This is test api
    """
    def get(self, request):
        return Response({'key': 'Hello World'})


class PostsView(ListCreateAPIView):
    authentication_classes = ()
    serializer_class = PostSerializer

    """
    Custom get list posts
    """
    def get_queryset(self):
        get_items = self.request.GET
        limit = get_items.get('limit')

        if limit is not None:
            limit = int(limit) - 1

        # Get list ids from redis
        list_comment_ids = r.zrange('comments', 0, limit, desc=True)

        """
        If list_comment_ids exists in redis, query list comments from list_comment_ids in posts table.
        Else, query directly from posts table
        """
        if len(list_comment_ids):
            return Post.objects.filter(id__in=list_comment_ids). \
                order_by('-total_comments')

        return Post.objects.order_by('-total_comments')

    """
    Create new post
    """
    def post(self, request):
        data = json.loads(request.body)
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = serializer.data

        """
        Add total_comments of new post to redis
        """
        r.zadd('comments', {str(response['id']): 0})

        return Response(response)


class PostView(GenericAPIView):
    authentication_classes = ()

    """
    Get a post by its id
    """
    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()

        if post is None:
            return Response(data={'code': 'not_found', 'message': 'Post not found'}, status=404)
        post_serializer = PostSerializer(instance=post)
        res = post_serializer.data

        return Response(res)


class CommentsView(ListCreateAPIView):
    authentication_classes = ()
    serializer_class = CommentSerializer

    """
    Custom get query set for comments
    """
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')

        return Comment.objects. \
            filter(post_id=post_id). \
            order_by('-created_at')

    """
    Create new comment for a post
    """
    def post(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()

        if post is None:
            return Response(data={'code': 'post_not_found', 'message': 'Post not found'}, status=404)
        data = json.loads(request.body)
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        """
        Get total comments value of post id from redis
        """
        total_comments = r.zscore('comments', str(post.id))

        """
        If value of total comments in redis is None, count it from db
        Else increase total comment with 1
        """
        if total_comments is None:
            total_comments = Comment.objects.filter(post_id=post_id).count()
        else:
            total_comments = int(total_comments) + 1

        """
        Update total comments value in redis
        """
        r.zadd('comments', {str(post.id): total_comments})

        response = serializer.data

        return Response(response)



