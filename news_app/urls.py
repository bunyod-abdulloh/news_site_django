from django.urls import path
from .views import NewsListView, NewsDetailView

urlpatterns = [
    path('all/', NewsListView.as_view(), name='all_news_list'),
    path('<int:id>/', NewsDetailView.as_view(), name='news_detail_page'),
]