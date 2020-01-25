from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ShowPostView.as_view(), name='post-home'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='post-delete'),
    path('post/add/', views.CreatePostView.as_view(), name='post-add'),
    path('post/<int:pk>/', views.show_post, name='post-detail'),
]
