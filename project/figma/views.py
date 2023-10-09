from tokenize import Comment
from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Post
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import PostForm

# Create your views here.




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'figma/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'figma/login.html', {'form': form}) 


def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    return render(request, 'figma/post_list.html', {'posts': posts, 'categories': categories})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'figma/post_detail.html', {'post': post})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'figma/category_list.html', {'categories': categories})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list') 
    else:
        form = PostForm()
    return render(request, 'figma/add_post.html', {'form': form})


def search(request):
    query = request.GET.get('q') 

    if query:
        results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    else:
        results = []

    return render(request, 'figma/search_results.html', {'results': results, 'query': query})

def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        # Создайте новый комментарий и сохраните его
        comment = Comment(text=request.POST['comment_text'], post=post)
        comment.save()
        return redirect('post_detail', post_id=post_id)
