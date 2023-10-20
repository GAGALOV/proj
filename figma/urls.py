from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
     path('add_post/', views.add_post, name='add_post'),
     path('search/', views.search, name='search'),
     path('posts/', views.PostListView.as_view(), name='posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)