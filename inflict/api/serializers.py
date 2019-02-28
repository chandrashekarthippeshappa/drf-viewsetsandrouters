from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models
from rest_framework import exceptions

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self,data):
        username = data.get("username","")
        password = data.get("password","")
        
        if username and password:
            user = authenticate(username = username,password = password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    message = "user is not Active"
                    raise exceptions.ValidationError(message)
            else:
                message = "username/password is wrong"
                raise exceptions.ValidationError(message)
        else:
            raise exceptions.ValidationError("Please provide username and password")
        
        return data 
    

        
class GroupSerializer(serializers.ModelSerializer):
    photo_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'group_id',
            'user',
            'group_name',
            'photo_count',
        )
        model = models.Group
        
    def get_photo_count(self, instance):
        return models.Photo.objects.filter(group=instance).count()


    
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'photo_id',
            'group',
            'photo_name',
            'photo',
            'uploaded_at',
        )
        model = models.Photo


class GroupDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'photo_id',
        )
        model = models.Photo
    
    
    


    
        
    
    


        


        
