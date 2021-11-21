from django.utils import timezone
from django.conf import settings

from config import celery_app

from .models import Todo


@celery_app.task()
def send_deadline_notifications() -> int:
    # get todos that are due in the next 1 hour, 
    # was not notified and author has email
    todos_to_notify = (
        Todo.objects.filter(
            notified=False, completed=False, deadline__gte=timezone.now() - settings.TODO_EMAIL_DEADLINE_AHEAD
        )
        .exclude(author__email__exact='')
        .only('id', 'deadline', 'author__email', 'title')
    )

    sent_emails_amount = 0
    for todo in todos_to_notify:
        try:
            todo.author.email_user(
                subject='Deadline for your task',
                message=f'Your task "{todo.title}" is due on {todo.deadline.strftime("%Y-%m-%d %H:%M")}',
            )
            todo.notified = True
            todo.save()
            sent_emails_amount += 1
        except Exception as e: # not sure what exceptions might occur
            print(f'Error sending email for todo {todo.id}: {e}')

    return sent_emails_amount

