from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import CommentorCreatorOrReadOnly
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from .serializer import *
from .models import *


# Create your views here.
class ThreadView(ViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
        except ValidationError as e:
            return Response({'info':e.message},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'info' : 'can not create a new thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(detail=True, methods=['GET'], url_path="get-comments")
    def get_comments(self,request, pk=None):
        """
            this functions return all the comments of the of the publisher site 
            here the pk will be the users website name which define in the user model
            and based on that field we filter the data of that users website from the backend here we query from the Thread model to the User model by using nested queries   
        """
        try:
            comments = Thread.objects.filter(post__created_by__website_name =pk)
        except Thread.DoesNotExist as e:
            return Response({'info':'no such comments exists !'},status=status.HTTP_401_UNAUTHORIZED)
        serializer = ThreadSerializer(comments,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    
class PostView(ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    model = Post

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info' : e.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def update(self,request,pk=None):
        try:
            post = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,post)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such post exits '},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk=None):
        try:
            post = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,post)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such post exits'},status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({'info':'post has been deleted successfully'},status=status.HTTP_200_OK)
    

class CommentView(ViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['GET','POST']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['DELETE','PUT']:
            self.permission_classes = [IsAuthenticated,CommentorCreatorOrReadOnly]
        return super().get_permissions()

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info': e.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(methods=['POST'],detail=False,url_path="comment-reply")
    def add_subcomment(self,request):
        data = request.data
        print(data)
        try:
            serializer = ReplyOnCommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info': e.message},status=status.HTTP_400_BAD_REQUEST)
        """ except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE) """
    
        


    def update(self,request,pk=None):
        try:
            comment = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,comment)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such comment exits '},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(comment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    def destroy(self,request,pk=None):
        try:
            comment = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,comment)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such comment exits'},status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response({'info':'comment has been deleted successfully'},status=status.HTTP_200_OK)
    
    
    @action(methods=['GET'],detail=True,url_path="comments")
    def get_comment_byusername(self,request,pk=None):
        """
            this function will filter the data of the comments that has been created by the user by filtering the data from the Thread table foe better formatting ans understanding the comment very well  
        """
        try:
            test = Thread.objects.filter(post__comments__created_by__username = pk)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such user exists !'})
        serializer = ThreadSerializer(test,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class PostLikeUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeUpdateSerializer

class PostOkUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostOkUpdateSerializer

class PostLovedUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLovedUpdateSerializer

class PostDislikeUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDislikeUpdateSerializer

class PostAngryUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostAngryUpdateSerializer