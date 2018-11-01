from .models import TodoListModel, UserModel
from rest_framework import serializers
from . import urls_name

class TodoListSerializer(serializers.ModelSerializer):
    """
        Class used for the JSON serialization and
        SQL deserialization
    """
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        """
            Class used as a Meta class to describe model and field
            from the model
        """
        model = TodoListModel
        fields = ('id', 'created', 'title', 'description', 'status', 'owner',)

class UserSerializer(serializers.ModelSerializer):
    """
        Class used for the JSON serialization and
        SQL deserialization
    """
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name=urls_name.TODO_DETAIL_NAME, read_only=True)

    class Meta:
        """
            Meta used to describe the serializer
            (fields, model, ...)
        """
        model = UserModel
        fields = ('id', 'email', 'password', 'is_ban', 'tasks', 'is_superuser',)
        read_only_fields = ('password',)
