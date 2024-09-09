from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import uuid, hashlib
import json
from django.db.models import Q
from .models import FriendRequest, Profile
from .serializers import (
    UserSerializer, SendRequestSerializer, FriendRequestSerializer,
    UserDisplaySerializer, TestingSerializer)


# class to exempt throttling - No request limit
class ExemptThrottle(SimpleRateThrottle):
    scope = 'exempt_scope'
    
    def allow_request(self, request, view):
        if view.__name__ == 'exempt_view':
            return True
        return super().allow_request(request, view)


class SignUp(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class SendFriendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendRequestSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request, format=None):
        serializer = SendRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            qs = FriendRequest.objects.filter(sender_id=self.request.user, recipient_id__id = serializer.data['recipient_id'])
            
            if qs.exists():
                return Response({"message": "Request already exist"}, status=status.HTTP_409_CONFLICT)
            
            if self.request.user.id==serializer.data['recipient_id']:
                return Response({"message": "Cannot send request to yourself"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            recipient_user = get_object_or_404(User, id=serializer.data['recipient_id'])
            FriendRequest.objects.create(
                sender_id = self.request.user,
                recipient_id = recipient_user, status='Pending'
                )
           
            response = {"message": "request sent successfully"}
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RespondOnRequest(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = FriendRequestSerializer
    lookup_field = 'pk'
    queryset = FriendRequest.objects.all()
    # throttling is exempt - No request limit
    throttle_classes = [ExemptThrottle]
    __name__ = 'exempt_view'
    
    def put(self, request, *args, **kwargs):
        qs = get_object_or_404(FriendRequest, id=kwargs.get('pk'))
        
        if qs.recipient_id.id == self.request.user.id:
            queryset = self.partial_update(request, *args, **kwargs)
            return queryset
        return Response({"message": "Operation not allowed"}, status=status.HTTP_403_FORBIDDEN)


class FriendsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = FriendRequestSerializer
    lookup_url_kwarg = "status"
    throttle_classes = [ExemptThrottle]
    __name__ = 'exempt_view'
    
    def get_queryset(self):
        request_status = self.kwargs.get(self.lookup_url_kwarg)
        if request_status=='Accepted':
            request_sender = FriendRequest.objects.filter(sender_id=self.request.user, status=request_status)
            return request_sender
        elif request_status=='Pending':
            request_sender = FriendRequest.objects.filter(sender_id=self.request.user, status=request_status)
            return request_sender


class SearchUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserDisplaySerializer
    throttle_classes = [ExemptThrottle]
    __name__ = 'exempt_view'
    
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        if query is None:
            raise APIException("Cannot Search")
        
        try:
            qs = User.objects.get(email=query)
            serializer =UserDisplaySerializer(qs)
            return Response(serializer.data)
        
        except User.DoesNotExist:
            search_result = User.objects.filter(email__icontains=query)
            serializer =UserDisplaySerializer(search_result, many=True)
            return Response(serializer.data)


def create_username(email):
    unique_id = uuid.uuid4()
    hash_object = hashlib.sha256(str(unique_id).encode())
    short_unique_id = hash_object.hexdigest()[:8]
    return email.split('@')[0]+short_unique_id+short_unique_id


test_users = [
    {
        "email" : "Amarendra@xy.com", 
        "password" : "test12345"
    },
    {
        "email" : "Amar@xy.com", 
        "password" : "test12345"
    },
    {
        "email" : "aman@xy.com", 
        "password" : "test12345"
    },
    {
        "email" : "Abhirama@xy.com", 
        "password" : "test12345"
    }
]
class AddUsersForTesting(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TestingSerializer
    throttle_classes = [ExemptThrottle]
    __name__ = 'exempt_view'
    
    def post(self, request, format=None):
        serializer = TestingSerializer(data=request.data)
        
        if serializer.is_valid(): 
            # with open('test_users.json') as f:
            #     user_json = json.load(f)

            for user in test_users:
                username = create_username(user['email'])
                password = make_password(user['password']),
                user = User(username=username, email=user['email'], password=password)
                user.save()
                Profile.objects.create(user=user)
            
            response = {"message": "users created"}
            return Response(response, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)