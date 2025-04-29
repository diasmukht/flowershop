from django.urls import path
from .views import profile, upgrade_status
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/upgrade/', upgrade_status, name='upgrade_status'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

