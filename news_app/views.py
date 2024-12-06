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


def news_detail(request, id):
    news = get_object_or_404(klass=News, pk=id, status=News.Status.Published)
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
        context['news_list'] = News.published.all().order_by('-publish_time')[:15]
        context['categories'] = self.model.objects.all()
        context['mahalliy_news'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[1:6]
        context['mahalliy_one'] = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:1]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        news_list =
        mahalliy_one =
        mahalliy_news =
        context = {
            'news_list': news_list,
            'categories': categories,
            "mahalliy_news": mahalliy_news,
            "mahalliy_one": mahalliy_one,
        }
        return self.render_to_response(context)


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
