from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Issue, Comment, IssueForm, CommentForm

def issue_index(request):
    # Here we show a list of open issues
    recent_issues = Issue().most_recent()

    return render(request, 'helpdesk/issue_index.html', {'recent_issues' : recent_issues})

def issue_show(request, issue_id):
    # Show a single issue
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm

    return render(request, 'helpdesk/issue_show.html', {'issue': issue, 'form': form})

def issue_create(request):
    # Show the form to create an issue
    form = IssueForm

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            """
            Future me should implement the submit using ajax
            return JsonResponse({'success': False,
                          'errors': [(k, v[0]) for k, v in form.errors.items()]})
            will return the error in a Json format
            """
            raise Exception('You have issues')

        return redirect('issue_index')

    return render(request, 'helpdesk/issue_form.html', { 'form' : form })

def issue_edit(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = IssueForm(instance = issue)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance = issue)
        if form.is_valid():
            form.save()
        else:
            """
            Future me should implement the submit using ajax
            return JsonResponse({'success': False,
                          'errors': [(k, v[0]) for k, v in form.errors.items()]})
            will return the error in a Json format
            """
            raise Exception('You have issues')

        return redirect('issue_index')

    return render(request, 'helpdesk/issue_form.html', {'form' : form})

def comment_create(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.issue = issue
        comment.save()
    else:
        """
        Future me should implement the submit using ajax
        return JsonResponse({'success': False,
                      'errors': [(k, v[0]) for k, v in form.errors.items()]})
        will return the error in a Json format
        """
        raise Exception('You have issues man!')

    return redirect('issue_show', issue_id)