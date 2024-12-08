from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Category, News
from .forms import ContactForm


def news_List(request):
    news = News.published.all()
    context = {
        'news_list': news,
    }

    return render(request, 'news/news_list.html', context)


def news_detail(request, news):
    news = get_object_or_404(klass=News, slug=news, status=News.Status.Published)
    context = {
        'news': news,
    }
    return render(request, 'news/news_detail.html', context)


def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')
    categories = Category.objects.all()
    context = {
        'news_list': news_list,
        'categories': categories,
    }
    return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['categories'] = Category.objects.all()
        context['mahalliy_news'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context['xorijiy_news'] = News.published.all().filter(category__name="Xorijiy").order_by('-publish_time')[:5]
        context['sports_news'] = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
        context['techno_news'] = News.published.all().filter(category__name="Texnologiya").order_by('-publish_time')[:5]

        return context


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(
                "<h2>Bizga habar yuborganingiz uchun tashakkur! Tez orada javob qaytarishga harakat qilamiz!</h2>")
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class MahalliyNewsView(ListView):
    name = News
    template_name = "news/mahalliy.html"
    context_object_name = "mahalliy_news"


class XorijiyNewsView(ListView):
    name = News
    template_name = "news/xorijiy.html"
    context_object_name = "xorijiy_news"


class TexnoNewsView(ListView):
    name = News
    template_name = "news/texno.html"
    context_object_name = "texno_news"


class SportNewsView(ListView):
    name = News
    template_name = "news/sport.html"
    context_object_name = "sport_news"
