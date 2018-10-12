from .models import TodoListModel, UserModel
from rest_framework import serializers

class TodoListSerializer(serializers.ModelSerializer):
    """
        Class used for the JSON serialization and
        SQL deserialization
    """
    class Meta:
        """
            Class used as a Meta class to describe model and field
            from the model
        """
        model = TodoListModel
        fields = ('id', 'created', 'title', 'description', 'status')

class UserSerializer(serializers.ModelSerializer):
    """
        Class used for the JSON serialization and
        SQL deserialization
    """
    class Meta:
        """
            Meta used to describe the serializer
            (fields, model, ...)
        """
        model = UserModel
        fields = ('id', 'email', 'password', 'is_ban',)
        read_only_fields = ('email', 'password',)
