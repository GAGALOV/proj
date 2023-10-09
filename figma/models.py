from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

from django.views import View


def uniq_name_upload(instance, filename):
    new_file_name = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    return f'post_images/{new_file_name}'

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
    image =  image = models.ImageField(upload_to='post_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    

class PostDetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.views_count += 1
        post.save()
        return render(request, 'post_detail.html', {'post': post})
    

