from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment