from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name="following", blank=True, symmetrical=False)

class Post(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.CharField(blank=False, max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")

    def serialize(self, current_user=None):
        return {
            "author": self.author.username,
            "id": self.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            # total number of likes
            "likes": len(self.likes.all()), 
            "body": self.body,
            # if current logged in user like the post
            "liked": current_user in self.likes.all() if current_user else False
        }
