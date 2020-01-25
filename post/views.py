from django.shortcuts import render
from .models import Post, Comment
from users.models import Profile
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PostSerialize, CommentSerialize, ProfileSerialize
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from .tasks import send_email_task
import json

from django.core.serializers import serialize 

class ShowPostView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'post'
    ordering = ['-date']

    def get_context_data(self, **kwards):
        ctx = super(ShowPostView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница блога'
        return ctx
def show_post(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post).order_by('-id')
    
    if request.method == 'POST':

        # print('---------------')
        # print(request.user.email)
        # print(post.author.email)
        # print('---------------')
        # quit()

        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            # comment = Comment.objects.create(post=post,user=request.user, content=content)
            # comment.save()

            to = post.author.email
            # user = 'sdd'
            # print('---------------')
            # str_data = serialize('json', request.user, cls=DjangoJSONEncoder)
            # print(type(request.user))
            # data = json.loads(request.user)
            # print(data)

            # print('---------------')
            # quit()
            send_email_task.delay(to, content)

            return HttpResponseRedirect(post.get_absolute_url())
        

    
    else:
        comment_form = CommentForm()
        
    return render(request,'post/post_detail.html',
                  {'post': post,'comments': comments,'comment_form': comment_form })



class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','img']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.img = self.request.FILES['img']

        return super().form_valid(form)



class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView ):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialize
    
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerialize
    
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerialize
    