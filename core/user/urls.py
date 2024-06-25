from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

routers = DefaultRouter()
routers.register('users',views.UserView)
routers.register('follow',views.FollowerViews)
urlpatterns = [
    path('',include(routers.urls)),
    path('auth',views.AuthenticationsView.as_view()),
    path('auth/user/<int:pk>/logout-user',views.AuthenticationsView.as_view()),
]
