from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.group_name
    
class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    photo_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to = 'images/', default = 'images/None/no-img.jpg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.photo_name




