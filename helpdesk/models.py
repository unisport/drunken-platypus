from django.db import models
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.contrib.auth.models import User


# Models
class Issue(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    ONHOLD = 'ONHOLD'

    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (ONHOLD, 'On Hold')
    )

    title = models.CharField(max_length=255)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default=OPEN,
        max_length=100
    )

    def comments(self):
        return Comment.objects.filter(issue_id=self.id).order_by('-created_at')

    @property
    def comment_count(self):
        return Comment.objects.filter(issue_id=self.id).count()

    @staticmethod
    def most_recent():
        # FIXME: Add the correct filtering
        return Issue.objects.filter().order_by('-created_at')


class UserActionHistory(models.Model):
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.CharField(max_length=255)
    fk = models.IntegerField(default=0)
    model_kind = models.CharField(max_length=100)


class Comment(models.Model):
    summary = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue)


class ChangeLog(models.Model):
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    @staticmethod
    def most_recent():
        return ChangeLog.objects.order_by('-created_at')[0:4]


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    topics = models.CharField(max_length=255)
    pinned = models.BooleanField(default=False)

    @staticmethod
    def most_recent():
        return Article.objects.filter(pinned=False).order_by('-created_at')[0:4]

    @staticmethod
    def most_recent_by_pinned():
        return Article.objects.order_by('-pinned', '-created_at')

    @staticmethod
    def pinned_articles():
        return Article.objects.filter(pinned=True).order_by('-created_at')[0:2]


# Signals
@receiver(post_init, sender=Issue, dispatch_uid='create_virgin_fields')
def create_virgin_fields(sender, instance, **kwargs):
    """This function adds a property to the model that stores the original
    values when instantiated or fetched from the database. If the model has no
    PK the property is_vigin is set to True
    """
    cached_values = {}
    track_fields = ('title', 'summary', 'status')
    for field in track_fields:
        cached_values[field] = getattr(instance, field)

    if getattr(instance, 'pk') is None:
        setattr(sender, 'is_virgin', True)
    else:
        setattr(sender, 'is_virgin', False)

    setattr(sender, 'track_fields', cached_values)


@receiver(post_save, sender=Issue, dispatch_uid='store_model_history')
def store_model_history(sender, instance, **kwards):
    """This function checks if the model is created or if changes have been
        made to an exising model. It's only the value of status that is stored
        as part of the message
    """
    track_fields = ('title', 'summary', 'status')

    if getattr(sender, 'is_virgin') is True:
        message = 'created a new {}'.format(
            instance.__class__.__name__
            )
        user_action = UserActionHistory(entry=message, author=instance.author,
                                        fk=instance.pk,
                                        model_kind=instance.__class__.__name__)

        user_action.save()
    else:
        for field in track_fields:
            if getattr(instance, field) != instance.track_fields[field]:
                if field != 'status':
                    message = 'changed {}'.format(
                            field
                        )
                else:
                    message = 'changed {} from {} to {}'.format(
                            field,
                            instance.track_fields[field],
                            getattr(instance, field)
                        )
                user_action = UserActionHistory(entry=message,
                                                author=instance.author,
                                                fk=instance.pk,
                                                model_kind=instance.__class__.__name__)

                user_action.save()


# ModelForms
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topics', 'pinned']
        fields_required = ['title', 'content']


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'summary', 'status']
        fields_required = ['title', 'summary']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['summary']
        fields_required = ['summary']


class ChangeLogForm(ModelForm):
    class Meta:
        model = ChangeLog
        fields = ['summary']
