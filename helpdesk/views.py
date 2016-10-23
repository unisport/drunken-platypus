from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import logging

from .models import Issue, Comment, ChangeLog, Article, IssueForm, CommentForm, ChangeLogForm, ArticleForm, UserActionHistory

def issue_index(request):
    # Here we show a list of open issues
    recent_issues = Issue().most_recent()
    recent_changelogentries = ChangeLog().most_recent()
    recent_articles = Article().most_recent()
    pinned_articles = Article().pinned_articles()

    return render(request, 'helpdesk/issue_index.html', {
        'recent_issues' : recent_issues,
        'recent_changelogentries' : recent_changelogentries,
        'recent_articles' : recent_articles,
        'pinned_articles' : pinned_articles
    })

def issue_show(request, issue_id):
    # Show a single issue
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm
    issue_history = UserActionHistory.objects.filter(fk=issue_id).order_by('-created_at')

    return render(request, 'helpdesk/issue_show.html', {'issue': issue, 'form': form, 'history': issue_history})

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
            issue = form.save()
        else:
            return JsonResponse({'success': False,
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            })

        return JsonResponse({'success': True})

    return render(request, 'helpdesk/issue_form.html', {'form' : form})

def comment_create(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.issue = issue
        comment.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False,
            'errors': [(k, v[0]) for k, v in form.errors.items()]
        })

def changelog_new(request):
    if request.method == 'POST':
        form = ChangeLogForm(request.POST)
        if form.is_valid():
            changelogentry = form.save(commit=False)
            changelogentry.author = ''
            changelogentry.save()
        else:
            raise Exception('You have issues man!')
        
        return redirect('issue_index')
    else:
        form = ChangeLogForm
        return render(request, 'helpdesk/changelog_form.html', {'form' : form})

def article_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            })
    else:
        form = ArticleForm

    return render(request, 'helpdesk/article_form.html', { 'form' : form })

def article_index(request):
    recent_articles = Article.most_recent_by_pinned()

    return render(request, 'helpdesk/article_index.html', { 'recent_articles' : recent_articles })

def article_show(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    return render(request, 'helpdesk/article_show.html', {'article': article})

def article_edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            })
    else:
        form = ArticleForm(instance=article)

    return render(request, 'helpdesk/article_form.html', {'form': form})

def article_topic(request, topic):
    articles = Article.objects.get(topics__icontains=topic)

    return render(request, 'helpdesk/article_topics.html', {'articles': articles, 'topic': topic})