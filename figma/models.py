from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import uuid

# Create your models here.

def uniq_name_upload(instance, filename):
    new_file_name = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    return f'images/{new_file_name}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name
    
class Blog(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to=uniq_name_upload)
    description = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.today())
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)     # !  1 #
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self) -> str:
        return self.name
    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    date = models.DateTimeField(default=datetime.datetime.today())
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=1)

