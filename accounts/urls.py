from django.urls import path
from .views import user_logout
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    # path('logout/', user_logout, name='logout'),
]
