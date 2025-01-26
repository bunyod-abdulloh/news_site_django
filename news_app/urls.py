from django.urls import path
from .views import ContactPageView, news_List, HomePageView, MahalliyNewsView, XorijiyNewsView, \
    TexnoNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view, SearchResultsList, \
    news_detail

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/create/', NewsCreateView.as_view(), name='news_create_page'),
    path('news/', news_List, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_edit_page'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('local/', MahalliyNewsView.as_view(), name='mahalliy_news_page'),
    path('foreign/', XorijiyNewsView.as_view(), name='xorijiy_news_page'),
    path('tech/', TexnoNewsView.as_view(), name='texno_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('admin-page/', admin_page_view, name='admin_page'),
    path('search-result/', SearchResultsList.as_view(), name='search_results'),
]
