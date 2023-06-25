from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Article
from home.http_util import generate_response



def list_articles(request: HttpRequest) -> HttpResponse:

    articles = Article.objects.all()

    context = {
        'articles': articles
    }

    response = generate_response(request, "blogs.html", context)
    return response


def display_article(request: HttpRequest, slug: str) -> HttpResponse:

    article = Article.objects.get(slug=slug)

    context = {
        'article': article
    }

    response = generate_response(request, "article.html", context)
    return response
