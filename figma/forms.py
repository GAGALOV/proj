from django import forms
from .models import *

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'category', 'image', 'description', 'date']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'fieldset button button-yellow input-file form-control'}),
            'description':forms.Textarea(attrs={'rows':5})
        }
        
    def sav(self, commit):
        author = settings.AUTH_USER_MODEL.objects.get(id=self.data['author_id'])
        self.instance.author = author
        return super().save()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'blog','text', 'date']
        widgets = {
            'description':forms.Textarea(attrs={'rows':3})
        }

class BlogSearchForm(forms.Form):
    search = forms.CharField(label='Поиск по блогам', max_length=100)    
