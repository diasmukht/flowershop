# constructor/urls.py
from django.urls import path
from . import views

app_name = 'constructor'  # Обязательно для пространства имён

urlpatterns = [
    path('', views.step_one, name='step1'),  # Страница выбора цветов и упаковки
    path('summary/', views.summary, name='summary'),  # Итоговая страница конструктора
    path('update_item/', views.update_item, name='update_item'),  # Обновление корзины через AJAX
    path('clear/', views.clear_constructor, name='clear_constructor'),  # Очистить корзину конструктора
    path('summary/partial/', views.summary_partial, name='summary_partial'),  # Частичное обновление корзины
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

]
