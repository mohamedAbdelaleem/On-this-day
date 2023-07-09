from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .models import Article
from .forms import ArticleForm
from utils.http_util import generate_response
from utils.media_files_util import delete_file


def list_articles(request: HttpRequest) -> HttpResponse:

    articles = Article.objects.all()
    delete_file("blabl/bal,.|a")
    context = {
        'articles': articles
    }

    response = generate_response(request, "blogs.html", context)
    return response


def display_article(request: HttpRequest, slug: str) -> HttpResponse:

    article = Article.objects.get(slug=slug)
    context = {
        'article': article,
    }

    response = generate_response(request, "article.html", context)
    return response


@permission_required("blog.add_article", raise_exception=True)
def add_article(request: HttpRequest) -> HttpResponse:

    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            author = request.user
            new_article.author = author
            new_article.save()
            return redirect('blog:display_article', slug=new_article.slug)

    
    context = {
        'form': form,
    }
    return render(request, 'add_article.html', context)


@permission_required("blog.change_article", raise_exception=True)
def edit_article(request: HttpRequest, slug: str) -> HttpResponse:

    article = Article.objects.get(slug=slug)
    if request.user.id != article.author.id:
        raise PermissionDenied

    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(data=request.POST, instance=article)
        if form.is_valid():
            form.save()
            
            return redirect('blog:display_article', slug=article.slug)

    
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'article_edit.html', context)


@permission_required("blog.delete_article", raise_exception=True)
def delete_article(request: HttpRequest, slug: str) -> HttpResponse:

    article = Article.objects.get(slug=slug)
    if request.user.id != article.author.id:
        raise PermissionDenied

    if request.method == "POST":
        article.delete()

    return redirect('blog:list_articles')

