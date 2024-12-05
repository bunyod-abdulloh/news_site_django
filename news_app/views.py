from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, News
from .forms import ContactForm


def news_list(request):
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
    news = News.published.all()
    categories = Category.objects.all()
    context = {
        'news': news,
        'categories': categories,
    }
    return render(request, 'news/index.html', context)


def contactPageView(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse("Bizga habar yuborganingiz uchun tashakkur! Tez orada javob qaytarishga harakat qilamiz!")
    context = {
        'form': form,
    }
    return render(request, 'news/contact.html', context)

# class NewsListView(ListView):
#     model = News
#     template_name = 'news/news_list.html'
#     context_object_name = 'news_list'
#
#     def get_queryset(self):
#         return News.published.all()  # Bu faqat nashr qilingan yangiliklarni ko'rsatadi
#
#
# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'
#     context_object_name = 'news'
#
#     def get_object(self, queryset=None):
#         # Bu faqat nashr qilingan yangilikni olishni ta'minlaydi
#
#         obj = super().get_object(queryset)
#         if obj.status != News.Status.Published:
#             raise Http404("Yangilik topilmadi yoki nashr qilinmagan.")
#         return obj
