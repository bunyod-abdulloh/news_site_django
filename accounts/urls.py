from django.urls import path
from .views import user_logout, dashboard_views
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', dashboard_views, name='user_profile'),
    path('password-change/', PasswordChangeView.as_view(success_url='/account/password-change-done/'),
         name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
