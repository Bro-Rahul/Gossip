from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('thread',views.ThreadView)
router.register('users-comments',views.CommentView)
router.register('post',views.PostView)

urlpatterns = [
    path('',include(router.urls)),

    path('posts/<int:pk>/like/', views.PostLikeUpdateView.as_view(), name='post-like-update'),
    path('posts/<int:pk>/ok/', views.PostOkUpdateView.as_view(), name='post-ok-update'),
    path('posts/<int:pk>/loved/', views.PostLovedUpdateView.as_view(), name='post-loved-update'),
    path('posts/<int:pk>/dislike/', views.PostDislikeUpdateView.as_view(), name='post-dislike-update'),
    path('posts/<int:pk>/angry/', views.PostAngryUpdateView.as_view(), name='post-angry-update'),
]