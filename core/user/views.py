from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .permissions import ActualUser
from user.models import *
from .serializer import *


class UserView(ViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in ['DELETE','PATCH']:
            self.permission_classes = [ActualUser]
        
        return super().get_permissions()

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail=False,url_path="create-publisher")
    def create_publishers(self,request):
        try:
            data = request.data
            serializer = PublisherSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as v:
            return Response({'info' : v.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' :'something went wrong'} ,status=status.HTTP_404_NOT_FOUND)
        
    @action(methods=['POST'],detail=False,url_path="create-commentor")
    def create_commentor(self,request):
        try:
            data = request.data
            print(request.data)
            serializer = CommenterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as v:
            return Response({'info' : v.message},status=status.HTTP_400_BAD_REQUEST)
        
        

    @action(methods=['GET'],detail=True,url_path="get-user")
    def retrieve_user(self, request, pk=None):
        try:
            user = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist as e:
            return Response({'info' : "No such user Exists"},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    @action(methods=['PATCH'],detail=False,url_path="update-user")
    def update_user(self,request):
        data = request.data
        id = data.get('id',None)
        try:
            user = self.model.objects.get(pk = int(id))
            self.check_object_permissions(request,user)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['DELETE'],detail=True,url_path="destroy-user")    
    def destroy_user(self, request, pk=None):
        try:
            user = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,user)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response({'info' : 'Your account has been deleted successfully!'},status=status.HTTP_200_OK)


class FollowerViews(ViewSet):
    model = Follower
    serializer_class = FollowerFollowingSerializer
    queryset = Follower.objects.all()

    def retrieve(self,request,pk=None):
        try:
            user = Follower.objects.get(pk=pk)
        except self.model.DoesNotExist as e:
            return Response({'info':'user does not exists'},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    @action(methods=['POST','GET'],detail=False,url_path='add-followers/user=(?P<user_id>\d+)/following=(?P<follower_id>\d+)')
    def add_followers(self, request, user_id=None, follower_id=None):
        if user_id and follower_id:
            user = User.objects.get(pk=user_id)
            follower = User.objects.get(pk=follower_id)
            follow,_ = self.model.objects.get_or_create(user = user,follower = follower)
            serializer = self.serializer_class(follow)

            return Response(serializer.data)
        else:
            return Response({"error": "user_id and follower_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.model.objects.get(pk=pk)
        user.delete()
        return Response({'info' : f'user {user.follower} unfollowed the user {user.user}'})
    
#THIS IS AN APIVIEW 
class AuthenticationsView(ObtainAuthToken): 

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
            self.permission_classes = [ActualUser]
        return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
            user_instance = User.objects.get(username = user)
        except User.DoesNotExist as e:
            return Response({'info':'no such user exists !'},status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user_instance)
        data = {
            'token':token.key,
            **user_serializer.data,
        }
        return Response(data,status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        try:
            user_token = Token.objects.get(user_id = pk)
            user = User.objects.get(pk = pk)
            self.check_object_permissions(request,user)
        except Token.DoesNotExist as e:
            return Response({'info':'no such user token exists '},status=status.HTTP_400_BAD_REQUEST)    
        user_token.delete()
        return Response({'info' : 'Logout successfully !'},status=status.HTTP_200_OK)