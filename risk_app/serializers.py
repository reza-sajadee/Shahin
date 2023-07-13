from rest_framework import serializers

from .models import RiskIdentification


class RiskIdentificationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = RiskIdentification
        fields = '__all__'
    

