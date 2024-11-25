from rest_framework import serializers
from .models import User, Subject, Unit

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_photo']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'sub_icon']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'unit_name', 'pdf_file', 'subject']


# In serializers.py
from rest_framework import serializers
from .models import Task
from rest_framework.exceptions import NotFound

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['created_at']

def create(self, validated_data):
        # Automatically associate task with user if user_id is provided
        user_id = validated_data.get('user_id')  # Retrieve user_id, not user
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User with the specified ID does not exist.")
        
        task = Task.objects.create(user=user, **validated_data)  # Pass the user object to the Task creation
        return task
def update(self, instance, validated_data):
    try:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    except Exception as e:
        raise serializers.ValidationError({"error": f"Failed to update task: {str(e)}"})
