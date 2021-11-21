from rest_framework import serializers

from apps.todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('author', 'title', 'description', 'deadline', 'priority', 'completed', 'created_at', 'updated_at')
