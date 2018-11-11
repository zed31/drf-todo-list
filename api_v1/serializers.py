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

    def create(self, validated_data):
        """
            Create a new User using validated data
        """
        user_instance = UserModel.objects.create_user(**validated_data)
        user_instance.save()
        return user_instance

    def update(self, instance, validated_data):
        """
            Update values from the instance thanks to the validated_data
            coming from the request

            :param instance: The instance of the User being updated
            :param validated_data: The validated data being used as reference
            :return: The edited instance
        """
        for attr, value in validated_data.items():
            instance.set_password(value) if attr == 'password' else setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        """
            Meta used to describe the serializer
            (fields, model, ...)
        """
        model = UserModel
        fields = ('id', 'email', 'password', 'is_ban', 'tasks', 'is_superuser',)
