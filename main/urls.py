from django.urls import path
from . import views  # Импорт views из текущего приложения
from .views import catalog_view
urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('bouquet/<int:id>/', views.bouquet_detail, name='bouquet_detail'),
    path('bouquet/<int:id>/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('gpt-response/', views.gpt_response, name='gpt_response'),
    path('catalog/', catalog_view, name='catalog'),

]
