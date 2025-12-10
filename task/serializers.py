from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=[
            'id',
            'title',
            'description',
            'priority',
            'status',
            'created_at',
        ]
        read_only_fields=['id','created_at']

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value    