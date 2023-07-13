from rest_framework import serializers

from .models import MeetingProfile


class MeetingProfileSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = MeetingProfile
        fields = ['meetingType' , 'title']
    

