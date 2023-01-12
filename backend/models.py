from django.db import models


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    body = models.TextField()
    total_comments = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'


class Comment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    body = models.TextField()
    path = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'
