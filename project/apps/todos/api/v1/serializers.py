from django.utils import timezone
from django.conf import settings

from rest_framework import serializers

from apps.todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'pk', 'author', 'title', 'description', 
            'deadline', 'priority', 'completed', 
            'created_at', 'updated_at', 'notified'
        )

    def to_internal_value(self, data: dict):
        data = data.copy()
        data['author'] = self.context['request'].user.pk
        return super().to_internal_value(data)

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Deadline must be in future')
        return value

    def create(self, validated_data):
        # if deadline date is inside notificating time 
        # set `notified` as True to not get notified by email
        if deadline := validated_data.get('deadline'):
            time_without_notificating = timezone.now() + settings.TODO_EMAIL_DEADLINE_AHEAD 
            if time_without_notificating > deadline:
                validated_data['notified'] = True

        instance = super().create(validated_data)

        return instance
    
    def update(self, instance, validated_data):
        # Check if new deadline date is inside notificating timedelta
        # if not inside set Todo as not notified
        if (deadline := validated_data.get('deadline')) and self.instance.notified:
            time_without_notificating = timezone.now() + settings.TODO_EMAIL_DEADLINE_AHEAD 
            if deadline > time_without_notificating:
                validated_data['notified'] = False
            else:
                validated_data['notified'] = True

        return super().update(instance, validated_data)
        