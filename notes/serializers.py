from rest_framework import serializers
from .models import User

# Serializer for User Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Ensure the email is unique
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        # Create the user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],  # Can still be blank or null
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Using email for login
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError({"error": "Both email and password are required."})

        return data
from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'sub_icon']
from rest_framework import serializers
from .models import Unit

class UnitSerializer(serializers.ModelSerializer):
    pdf_file = serializers.FileField(required=True)

    class Meta:
        model = Unit
        fields = ['id', 'unit_name', 'pdf_file', 'subject']
