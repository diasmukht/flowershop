# FlowersShop/urls.py
from django.contrib import admin
from django.urls import path, include
from main import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.core.management import call_command
from django.http import HttpResponse



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),  # Главная страница
    path('', include('main.urls')),           # Все остальные страницы из приложения main
    path('users/', include('users.urls')),    # Аутентификация пользователей
    path('constructor/', include(('constructor.urls', 'constructor'), namespace='constructor')),  # Конструктор букетов

]

# Подключаем доступ к медиа-файлам (для картинок цветов, упаковки и пр.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
