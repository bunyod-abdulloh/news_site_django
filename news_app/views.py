from django.shortcuts import render
from .models import Category, News


def news_list(request):
    news = News.objects.all()
    context = {
        'news_list': news,
    }

    return render(request, 'news/news_list.html', context)
