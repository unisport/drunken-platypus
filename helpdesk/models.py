from django.db import models
from django.forms import ModelForm

# Models
class Issue(models.Model):
    OPEN = 'OPEN'
    RESOLVED = 'RESOLVED'
    REOPENED = 'REOPENED'
    ONHOLD = 'ONHOLD'
    
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (RESOLVED, 'Resolved'),
        (REOPENED, 'Reopened'),
        (ONHOLD, 'On Hold')
    )

    title = models.CharField(max_length=255)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # FIXME: Should be logged in user
    author = models.CharField(max_length=100)
    kb = models.BooleanField(default=False)
    status = models.CharField(
        choices = STATUS_CHOICES,
        default = OPEN,
        max_length = 100
    )

    def comments():
        return Comment.objects.filter(issue_id=self.id).order_by('-created_at')

    @staticmethod
    def most_recent():
        # FIXME: Add the correct filtering
        return Issue.objects.filter().order_by('-created_at')

class Comment(models.Model):
    summary = models.TextField()
    # FIXME: Should be logged in user
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue)

# ModelForms
class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'summary', 'status']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['summary']