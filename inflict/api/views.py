
from rest_framework.views import APIView
from . import models,serializers
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

@permission_classes((AllowAny,))    
class LoginViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    def create(self,request):
        serializer = serializers.LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data["user"]
        django_login(request,user)
        token,created = Token.objects.get_or_create(user = user)
        return Response({"token":token.key,"status":200})
    
        
class GroupsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get']
    
    def list(self, request, format=None):
        queryset = models.Group.objects.filter(user = request.user.id )
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = serializers.GroupSerializer(result_page, many=True,context={'request':request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response


class GroupDetailsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get']
    def retrieve(self,request,format=None,pk=None):
        queryset = models.Photo.objects.filter(group__user = request.user.id,group=pk)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = serializers.GroupDetailsSerializer(result_page, many=True,context={'request':request})
        response = Response(serializer.data , status=status.HTTP_200_OK)
        return response

class GroupPhotosViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get']
    def list(self, request, *args, **kwargs):
        GID = request.GET.get('group', None)
        if GID is not None:
            queryset = models.Photo.objects.filter(group__user=request.user.id,group=GID)
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = serializers.PhotoSerializer(result_page, many=True,context={'request':request})
            response = Response(serializer.data, status=status.HTTP_200_OK)
            return response
#         return super(GroupPhotosViewSet, self).list(request, *args, **kwargs)

class PhotoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    def retrieve(self,request, format=None,pk=None):
        queryset = models.Photo.objects.filter(group__user=request.user.id,pk=pk)
        serializer = serializers.PhotoSerializer(queryset, many=True)
        return Response(serializer.data)


class LogoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get']
    def list(self,request):
        request.user.auth_token.delete()
        django_logout(request)
        return Response({"message":"Successfully logged out."},status = 204)

