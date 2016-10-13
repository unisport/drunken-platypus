from django.db import models

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