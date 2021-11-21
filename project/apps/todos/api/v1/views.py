from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from apps.accounts.permissions import IsEmployeeOrReadOnly
from apps.todos.models import Todo
from apps.utils.permissions import IsRelated

from .serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    """
    Provides full CRUD functionality for Todo model
    Reading is allowed for all authenticated users
    Creating only for users with Employee type
    Updating and deleting allowed for Todo author and admin users
    """

    permission_classes = [IsAuthenticated]
    user_field = 'author'  # for `IsRelated` Permission class

    queryset = Todo.objects.prefetch_related('author').all()
    serializer_class = TodoSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS or self.action == 'create':
            self.permission_classes.append(IsEmployeeOrReadOnly)
        else:
            self.permission_classes.append(IsRelated)

        return super().get_permissions()
