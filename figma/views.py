from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView     
from rest_framework.viewsets import ModelViewSet  
from rest_framework.decorators import action 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponse
from rest_framework.views import APIView     
from rest_framework.response import Response 
from django.views.generic import View
from .permissions import *
from .models import *
from .forms import *
from .serializer import *
from django.http import Http404


menu = [
    {'title':'Home', 'url':'figma:home'},
    {'title':'Description', 'url':'figma:category'},   
    {'title':'Регистрация', 'url':'authe:signup'},
    {'title':'Вход', 'url':'authe:signin'},
]

def Home(request):
    data = {
        'title':'Главная',
        'menu': menu,
        'categories': Category.objects.all(),
        'blogs': Blog.objects.all(),
    }
    return render(request, 'figma/home.html',  data)


class CategoriesBlog(ListView):
    model = Blog
    template_name = 'figma/home.html'
    context_object_name = 'categories'
    

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        # Передача контекстных данных  #
        context['title'] = 'Категории'
        context['menu'] = menu
        context['categories'] = Category.objects.all()

        return context
    
def site_category(request, category_id):
    blogs = Blog.objects.filter(category_id=category_id)
    categories = Category.objects.all()

    data = {
        'blogs':blogs,
        'categories':categories,
        'menu':menu,
        'title':'Статьи',
        'category_id':category_id
    }

    return render(request, 'figma/home.html', context=data) 


class AddBlog(CreateView):
    form_class = BlogForm
    template_name = 'figma/add_blog.html'
    success_url = reverse_lazy('figma:home.html')   

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Новый блог'
        context['menu'] = menu

        return context

def delete_blog(request, blog_id):           
    try:
        blog = Blog.objects.get(pk=blog_id)
        blog.delete()
        return redirect('authe:profile')    
    except Blog.DoesNotExist:
        return HttpResponse("Blog DoesNotExist") 

class EditBlog(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'figma/redact.html'  
    success_url = reverse_lazy('figma:home')
    
    def get_object(self):
        blog_id = self.kwargs['blog_id']
        return Blog.objects.get(pk=blog_id)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
def profile(request):
    user = request.user
    user_blogs = Blog.objects.filter(author=user)

    return render(request, 'profil.html', {'user_blogs': user_blogs})


class BlogSearchView(View):
    template_name = 'figma/home.html'

    def post(self, request):
        form = BlogSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search']    
            blogs = Blog.objects.filter(name__icontains=search_query)  
            return render(request, 'figma/home.html', {'blogs':blogs, 'query':search_query})
        return render(request, self.template_name, {'form':form})

class AddComment(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'figma/add_comment.html'
    success_url = reverse_lazy('figma:home')    
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        blog_id = self.kwargs.get('blog_id')

        if blog_id:                               
            form.instance.blog_id = blog_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый комментарий'
        context['menu'] = menu

        return context
    
def delete_comment(request, blog_id):           
    try:
        comment = Comment.objects.get(pk=blog_id)
        comment.delete()
        return redirect('figma:home')   
    except Comment.DoesNotExist:
        return HttpResponse("Comment DoesNotExist") 


class ShowComment(DetailView):
    model = Comment                     
    template_name = 'figma/comentary.html'
    pk_url_kwarg = 'comment_id'

    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(blog_id=self.blog_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обзор комментариев'
        context['blog'] = Blog.objects.get(id=self.blog_id)
        context['menu'] = menu
        return context
    

class BlogDetail(DetailView):
    model = Blog
    template_name = 'figma/commentary.html'
    pk_url_kwarg = 'blog_id'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обзор блога'
        context['comments'] = Comment.objects.filter(blog_id=self.kwargs['blog_id']) 
        context['categories'] = Category.objects.all()
        context['menu'] = menu
        return context


               

class BlogListAPIView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAdminOrReadOnly,)    


class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrReadOnly,) 



class CommentListAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,)

class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,) 

