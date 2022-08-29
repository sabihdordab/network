from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='posts')
    title = models.TextField(blank=True)
    content = models.TextField(blank=False)
    date = models.DateField(default=datetime.now())

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
