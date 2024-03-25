from django.forms import ModelForm
from .models import Post
from django import forms



class PostUploadForm(ModelForm):
    caption = forms.CharField(widget= forms.Textarea
                           (attrs={'placeholder':'Caption'}))
    
    image = forms.ImageField()
    
    # def save(self, commit=True,*args, **kwargs):
    #     self.cleaned_data['user']=kwargs['user']
    #     return super(PostUploadForm, self).save(commit=commit)

    class Meta:
        model = Post
        fields = ['image','caption',]
         

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget= forms.TextInput(attrs={'placeholder':'Search for users'}))


 