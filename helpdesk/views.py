from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Issue, Comment, ChangeLog, Article, IssueForm
from .models import CommentForm, ChangeLogForm, ArticleForm, UserActionHistory


@login_required
def issue_index(request):
    recent_issues = Issue().most_recent()
    recent_changelogentries = ChangeLog().most_recent()
    recent_articles = Article().most_recent()
    pinned_articles = Article().pinned_articles()

    return render(request, 'helpdesk/issue_index.html', {
        'recent_issues': recent_issues,
        'recent_changelogentries': recent_changelogentries,
        'recent_articles': recent_articles,
        'pinned_articles': pinned_articles
    })


@login_required
def issue_show(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm
    # FIXME query shouldn't be in the view, I like my models to be fat!
    # Fat models and skinny views! Yeahh!
    issue_history = UserActionHistory.objects.filter(
                                        fk=issue_id).order_by('-created_at')

    return render(request, 'helpdesk/issue_show.html', {'issue': issue,
                                                        'form': form,
                                                        'history': issue_history})


@login_required
def issue_create(request):
    form = IssueForm

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.author = request.user
            issue.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                        'errors': [(k, v[0]) for k, v in form.errors.items()]})

    return render(request, 'helpdesk/issue_form.html', {'form': form})


@login_required
def issue_edit(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = IssueForm(instance=issue)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue.author = request.user
            issue = form.save()
        else:
            return JsonResponse({'success': False,
                        'errors': [(k, v[0]) for k, v in form.errors.items()]})

        return JsonResponse({'success': True})

    return render(request, 'helpdesk/issue_form.html', {'form': form})


@login_required
def comment_create(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.issue = issue
        comment.author = request.user
        comment.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False,
            'errors': [(k, v[0]) for k, v in form.errors.items()]
        })


@login_required
def changelog_new(request):
    if request.method == 'POST':
        form = ChangeLogForm(request.POST)
        if form.is_valid():
            changelogentry = form.save(commit=False)
            changelogentry.author = request.user
            changelogentry.save()
        else:
            raise Exception('You have issues man!')

        return redirect('issue_index')
    else:
        form = ChangeLogForm
        return render(request, 'helpdesk/changelog_form.html', {'form': form})


@login_required
def article_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            })
    else:
        form = ArticleForm

    return render(request, 'helpdesk/article_form.html', {'form': form})


@login_required
def article_index(request):
    recent_articles = Article.most_recent_by_pinned()

    return render(request, 'helpdesk/article_index.html', {'recent_articles': recent_articles})


@login_required
def article_show(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    return render(request, 'helpdesk/article_show.html', {'article': article})


@login_required
def article_edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,
                'errors': [(k, v[0]) for k, v in form.errors.items()]
            })
    else:
        form = ArticleForm(instance=article)

    return render(request, 'helpdesk/article_form.html', {'form': form})


@login_required
def article_topic(request, topic):
    """Currently not implemented. The idea is to let users filter articles based
    on a topic. A topic could be something like 'how to do stuff' or knowledge related
    to specific areas of the platform
    """
    articles = Article.objects.get(topics__icontains=topic)

    return render(request, 'helpdesk/article_topics.html',
                                        {'articles': articles, 'topic': topic})
