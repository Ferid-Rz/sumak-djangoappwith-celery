from rest_framework import serializers
from .models import Post,Comment
from users.models import Profile
        
class ProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','img','user')
        
class CommentSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'timestamp', 'post','user_id')
        
        
class PostSerialize(serializers.ModelSerializer):
    comments = CommentSerialize(many=True)
    class Meta:
        model = Post
        fields = ('id','title', 'text', 'img','date', 'author','comments')