from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories','image']
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
        'content': forms.Textarea(attrs={'placeholder': 'Содержание поста'}),
        'categories': forms.Select(attrs={'placeholder': 'Выберите категории'}),
        'image': forms.ClearableFileInput(attrs={'placeholder': 'Загрузите изображение'})
        }