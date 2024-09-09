from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile, FriendRequest
from rest_framework.generics import get_object_or_404
import uuid, hashlib, random


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, allow_blank=False, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        write_only_fields = ('password')
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those password don't match.")
        return attrs
    
    # Prevent different account with same email_id
    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exist")
        return value
    
    def create(self, validated_data):
        unique_id = uuid.uuid4()
        hash_object = hashlib.sha256(str(unique_id).encode())
        short_unique_id = hash_object.hexdigest()[:8]
        
        user = User.objects.create(
            username = validated_data['email'].split('@')[0]+short_unique_id,
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            is_active=True,
        )

        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'


class UserDisplaySerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'profile']
    
    def get_profile(self,obj):
        try:
            profile_instance = Profile.objects.get(user=obj)
            return ProfileSerializer(profile_instance).data
        except Profile.DoesNotExist:
            return None


class SendRequestSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField(required=True)


class FriendRequestSerializer(serializers.ModelSerializer):
    recipient_detail = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['sender_id', 'recipient_id']
        
    
    def get_recipient_detail(self, obj):
        recipent_user = get_object_or_404(User, id=obj.recipient_id.id)
        
        return UserDisplaySerializer(recipent_user).data


class TestingSerializer(serializers.Serializer):
    test = serializers.CharField()