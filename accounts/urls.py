from django.urls import path
from .views import user_logout, dashboard_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', dashboard_views, name='user_profile'),
]
