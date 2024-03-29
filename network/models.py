from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='posts')
    title = models.TextField(blank=True)
    content = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE , related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers" )
    def __str__(self):
        return f"{self.user} is following {self.user_followed}"
    def get_user_followed_posts(self):
        return self.user_followed.posts.order_by("-date").all()
