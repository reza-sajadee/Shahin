from rest_framework import serializers

from .models import Notifications


class NotificationstSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notifications
        fields = ['title', 'sender', 'sender', 'created_at']
    

