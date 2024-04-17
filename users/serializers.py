from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Model Serializer for User. """

    class Meta:
        model = User
        fields = '__all__'
