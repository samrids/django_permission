from rest_framework import serializers
from userprofile.models import Profile

# Serializers define the API representation.

class AvatarSerializer(serializers.ModelSerializer):  
       
    class Meta:
        model = Profile
        fields = ['avatar'] 

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save(update_fields=['avatar']) #Specify which fields to save
        return instance
                 

class ProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    avatar_url = serializers.SerializerMethodField(read_only=True)

    userid =  serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Profile
        fields = ('id', 'userid', 'username', 'email', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'age', 'adult', 'bio_text', 'status_text', 'avatar_url')
        read_only_fields = ('avatar_url', 'username', 'first_name', 'last_name', 'email', 'mobile')


    def get_userid(self, instance):
        if instance.user:
            return instance.user.id
        return None

    def get_username(self, instance):
        if instance.user:
            return instance.user.username
        return None

    def get_email(self, instance):
        if instance.user:
            return instance.user.email
        return None

    def get_first_name(self, instance):
        if instance.user:
            return instance.user.first_name
        return None

    def get_last_name(self, instance):
        if instance.user:
            return instance.user.last_name
        return None                        

    def get_age(self, instance):
        return instance.age

    def get_avatar_url(self, instance):
        current_site = '127.0.0.1:8000'
        if instance.avatar:
            return 'http://{0}{1}'.format(current_site, instance.avatar.url)
        return None
            
        

    def update(self, instance, validated_data):        
        
        updateFields = []
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            updateFields.append(attr)
                                                
        def is_adult():
            import datetime
            instance.adult = ((datetime.date.today() - instance.date_of_birth) > datetime.timedelta(days=18*365))                 

        if not instance.date_of_birth is None:
            is_adult()                        

        instance.save(update_fields= updateFields)
        return instance
