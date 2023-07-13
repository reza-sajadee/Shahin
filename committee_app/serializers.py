from rest_framework import serializers

from .models import Committee


class CommitteetSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Committee
        fields = '__all__'
    

