from django.db import connection


def update_total_comments():
  print('hello world')
  with connection.cursor() as cursor:
      query = "UPDATE public.posts p SET total_comments = c.total_comments from (select count(id) as total_comments, post_id from public.comments group by post_id) c where p.id = c.post_id";
      cursor.execute(query)
      # row = cursor.fetchone()