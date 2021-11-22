from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsEmployeeOrReadOnly
from apps.todos.models import Todo
from apps.utils.permissions import IsRelatedOrAdmin

from .serializers import TodoSerializer


SAFE_ACTIONS = ['list', 'retrieve']


class TodoViewSet(ModelViewSet):
    """
    Provides full CRUD functionality for Todo model
    Reading is allowed for all authenticated users
    Creating only for users with Employee type
    Updating and deleting allowed for Todo author and admin users
    """

    queryset = Todo.objects.prefetch_related('author').all()
    serializer_class = TodoSerializer

    @property
    def permission_classes(self):
        permissions = [IsAuthenticated, IsEmployeeOrReadOnly]
        if self.action not in SAFE_ACTIONS:
            permissions.append(IsRelatedOrAdmin)
        return permissions

    user_field = 'author'  # for `IsRelatedOrAdmin` Permission class
