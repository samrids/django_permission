from django.contrib.auth import authenticate
# from pkg_resources import require
from rest_framework import serializers

from django.contrib.auth.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={"input_type": "password"},
    )

    first_name = serializers.CharField(
        max_length=150,
        required=True,
    )

    last_name = serializers.CharField(
        max_length=150,
        required=True,        
    )    
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']
        read_only_fields = ('id',)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)
        
        
    def create_user(self, username, email, password,first_name, last_name,is_active):
        # this is a separate method so it's easy to override
        return User.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            is_active=is_active,
            first_name=first_name, 
            last_name=last_name)
        

    def save(self):
        username = self.validated_data["username"]        
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        first_name=self.validated_data["first_name"]
        last_name=self.validated_data["last_name"]

        user = self.create_user(
            username, 
            email, 
            password, 
            first_name, 
            last_name,
            is_active=False,)       

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name','last_name')

    def update(self, instance, validated_data):        
        
        updateFields = []
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            updateFields.append(attr)                                                                     

        instance.save(update_fields= updateFields)
        return instance
