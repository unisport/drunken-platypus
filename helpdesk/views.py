from django.shortcuts import render, get_object_or_404, redirect

from .models import Issue, Comment, IssueForm, CommentForm

def issueIndex(request):
    # Here we show a list of open issues
    recent_issues = Issue.objects.order_by('-status', '-created_at').filter(status__in = [Issue.OPEN, Issue.ONHOLD, Issue.REOPENED])

    return render(request, 'helpdesk/issue_index.html', {'recent_issues' : recent_issues})

def issueShow(request, issue_id):
    # Show a single issue
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm

    return render(request, 'helpdesk/issue_show.html', {'issue': issue, 'form': form})

def issueCreate(request):
    # Show the form to create an issue
    form = IssueForm

    if request.POST:
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('issue_index')

    return render(request, 'helpdesk/issue_form.html', { 'form' : form })

def issueEdit(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = IssueForm(instance = issue)

    if request.POST:
        form = IssueForm(request.POST, instance = issue)
        if form.is_valid():
            form.save()

        return redirect('issue_index')

    return render(request, 'helpdesk/issue_form.html', {'form' : form})

def commentCreate(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()

    return redirect('issue_show', issue_id)