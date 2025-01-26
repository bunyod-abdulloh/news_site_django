from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from hitcount.utils import get_hitcount_model

from .custom_permissions import OnlyLoggedSuperUser
from .models import Category, News
from .forms import ContactForm, CommentForm


def news_List(request):
    news = News.published.all()
    context = {
        'news_list': news,
    }

    return render(request, 'news/news_list.html', context)


from hitcount.views import HitCountDetailView, HitCountMixin


class PostCountHitDetailView(HitCountDetailView):
    model = News  # your model goes here
    count_hit = True


def news_detail(request, news):
    news = get_object_or_404(klass=News, slug=news, status=News.Status.Published)
    context = {}

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_count'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)  # Redirect to avoid duplicate submissions

    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
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

    def get_queryset(self):
        news = News.published.all().filter(category__name="Mahalliy")
        return news


class XorijiyNewsView(ListView):
    name = News
    template_name = "news/xorijiy.html"
    context_object_name = "xorijiy_news"

    def get_queryset(self):
        news = News.published.all().filter(category__name="Xorijiy")
        return news


class TexnoNewsView(ListView):
    name = News
    template_name = "news/texno.html"
    context_object_name = "texno_news"

    def get_queryset(self):
        news = News.published.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    name = News
    template_name = "news/sport.html"
    context_object_name = "sport_news"

    def get_queryset(self):
        news = News.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news_edit.html'
    # slug_field = 'slug'  # Slug ustuni nomi
    # slug_url_kwarg = 'slug'  # URL'dan olinadigan parametr


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


# class NewsCreateView(CreateView):
#     model = News
#     template_name = 'crud/news_create.html'
#     fields = ('title', 'slug', 'image', 'category', 'body', 'status', )

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'image', 'category', 'body', 'status',)
    success_url = reverse_lazy('news_list')  # Yaratilgandan so'ng qaytariladigan sahifa

    def form_valid(self, form):
        # Agar `slug` bo'sh bo'lsa, avtomatik yaratiladi
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.published.filter(
            Q(
                title__icontains=query
            ) |
            Q(
                body__icontains=query
            )
        )
