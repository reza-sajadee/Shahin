from rest_framework import serializers

from .models import JobBank , TypePostSazmani


class OrgSerializer(serializers.ModelSerializer):
    jobBankPost = serializers.SlugRelatedField(
        
        read_only=True,
        slug_field='title'
     )
    jobBankPostMafogh = serializers.SlugRelatedField(
        
        read_only=True,
        slug_field='postMafogh'
     )


    class Meta:
        model = JobBank
        fields = ['jobBankPost', 'jobBankPostMafogh']
    




class JobSerializer(serializers.ModelSerializer):
 

    class Meta:
        model = TypePostSazmani
        fields = ['title' ]
    
