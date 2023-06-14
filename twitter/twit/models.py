from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Post(models.Model):
    post_text = models.TextField()
    pabe_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static/image")


class Сomments(models.Model):
    сomments_text = models.CharField(max_length=200)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.сomments_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=580)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tweet {self.id} by {self.user.username}'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='static/image', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='static/image', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.user.username}'
