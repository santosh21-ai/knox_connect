from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid

REQUEST_STATUS=[
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Reject", "Reject")
]

class Profile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to="PROFILE PHOTO", blank=True, null=True)
    dob = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user.username


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_sender")
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_receiver")
    status = models.CharField(choices=REQUEST_STATUS, max_length=20, default="Not set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.sender_id.email +' to '+self.recipient_id.email


class FriendShip(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_two')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user_one.email +' and '+self.user_two.email