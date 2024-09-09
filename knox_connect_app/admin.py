from django.contrib import admin
from .models import Profile, FriendRequest, FriendShip


admin.site.register([
    Profile, FriendRequest, FriendShip
])