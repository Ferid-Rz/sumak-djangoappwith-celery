from django import forms
from .models import Post, Comment

class PostImage(forms.ModelForm):
    def __init__(self, *args, **kwards):
        super(PostImage, self).__init__(*args, **kwards)
        self.fields['img'].label = "Post picture"
    class Meta:
        model = Post
        fields = ['img']
        
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Text goes here!!!','rows':4,'cols':50}))
    class Meta:
        model = Comment
        fields = {'content'}