from django.urls import path, re_path
from . import views

urlpatterns = [
    path('sign-up', views.SignUp.as_view(), name='signUp'),
    path('send-friend-request', views.SendFriendRequest.as_view(), name='sendFriendRequest'),
    path('respond-on-request/<str:pk>', views.RespondOnRequest.as_view(), name='respondOnRequest'),
    
    path('friends-list/<str:status>', views.FriendsList.as_view(), name='friendsList'),
    path('search-users/', views.SearchUsers.as_view(), name='searchUsers'),
    
    path('add-users-for-testing', views.AddUsersForTesting.as_view(), name='addUsersForTesting'),
    
]