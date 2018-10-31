from rest_framework import serializers
from .. import models

class UserSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = ('password', )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        #fields = ('username', 'email', 'password')
        # Allow write it, but do not return it in serialization
        extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'
#        exclude = ('password', )

    def create(self, validated_data):
#        user = models.User(
#            email=validated_data.get('email', None)
#        )
#        user.set_password(validated_data.get('password', None))
#        user.save()
#        return user
        #return models.User.objects.create_user(validated_data['email'],validated_data['password'],**validated_data)

#        email = validated_data.get("email", None)
#        validated_data.pop("email")
#        return models.User.objects.create_user(email=email,**validated_data)

        return models.User.objects.create_user(**validated_data)
