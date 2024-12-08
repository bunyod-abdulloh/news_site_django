from django.urls import path
from .views import news_detail, ContactPageView, news_List, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_List, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
]
