# FlowersShop/urls.py
from django.contrib import admin
from django.urls import path, include
from main import views as main_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls')),    # Аутентификация пользователей
    path('constructor/', include(('constructor.urls', 'constructor'), namespace='constructor')),  # Конструктор букетов
   
]

# Подключаем доступ к медиа-файлам (для картинок цветов, упаковки и пр.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
