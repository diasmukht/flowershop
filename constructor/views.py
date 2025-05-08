from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from main.models import CartItem
from .models import (
    CustomBouquet, CustomBouquetFlower, CustomBouquetGreenery, CustomBouquetPackaging,
    Flower, Greenery, Packaging
)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json


def step_one(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    flowers = Flower.objects.filter(available=True)
    greenery = Greenery.objects.filter(available=True)
    wraps = Packaging.objects.all()

    bouquet = CustomBouquet.objects.filter(session_key=session_key).last()

    total_flowers = 0
    if bouquet:
        total_flowers = sum(item.quantity for item in bouquet.custombouquetflower_set.all())

    return render(request, 'constructor/constructor_step1.html', {
        'flowers': flowers,
        'greenery': greenery,
        'wraps': wraps,
        'bouquet': bouquet,
        'total_flowers': total_flowers

    })


def summary(request):
    session_key = request.session.session_key
    bouquet = CustomBouquet.objects.filter(session_key=session_key).last()
    if not bouquet:
        return redirect('constructor:step1')

    bouquet.update_total_price()

    total_flowers = sum(item.quantity for item in bouquet.custombouquetflower_set.all())

    return render(request, 'constructor/summary.html', {
        'bouquet': bouquet,
        'items': bouquet.custombouquetflower_set.select_related('flower'),
        'total_flowers': total_flowers
    })


@csrf_exempt
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_type = data['type']
        item_id = int(data['id'])
        action = data['action']

        session_key = request.session.session_key
        bouquet, _ = CustomBouquet.objects.get_or_create(session_key=session_key)

        if item_type == 'flower':
            model = CustomBouquetFlower
            base_model = Flower
            field = 'flower'

            base_obj = base_model.objects.get(id=item_id)

            # Ограничение: не более 5 видов цветов
            existing_flower_ids = bouquet.custombouquetflower_set.values_list('flower_id', flat=True)
            if action == 'add' and base_obj.id not in existing_flower_ids and len(existing_flower_ids) >= 5:
                return JsonResponse({'error': 'Можно выбрать не более 5 разных цветов'}, status=400)

        elif item_type == 'greenery':
            model = CustomBouquetGreenery
            base_model = Greenery
            field = 'greenery'
        elif item_type == 'packaging':
            model = CustomBouquetPackaging
            base_model = Packaging
            field = 'packaging'

            if action == 'add':
                model.objects.filter(custom_bouquet=bouquet).delete()
        else:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        base_obj = base_model.objects.get(id=item_id)
        item, created = model.objects.get_or_create(custom_bouquet=bouquet, **{field: base_obj})

        if action == 'add':
            item.quantity = 1 if item_type == 'packaging' else item.quantity + 2
        elif action == 'remove':
            item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

        bouquet.update_total_price()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
def clear_constructor(request):
    session_key = request.session.session_key
    if session_key:
        CustomBouquet.objects.filter(session_key=session_key).delete()
    return redirect('constructor:step1')


def summary_partial(request):
    session_key = request.session.session_key
    bouquet = CustomBouquet.objects.filter(session_key=session_key).last()
    if not bouquet:
        return HttpResponse("")

    bouquet.update_total_price()
    has_packaging = bouquet.custombouquetpackaging_set.exists()
    total_flowers = 0
    bouquet_size = request.session.get('bouquet_size')

    if bouquet:
        total_flowers = sum(item.quantity for item in bouquet.custombouquetflower_set.all())

    html = render_to_string('constructor/_summary_mini.html', {
        'bouquet': bouquet,
        'total_flowers': total_flowers,
        'has_packaging': has_packaging,
        'bouquet_size': bouquet_size
    })
    return HttpResponse(html)


def add_to_cart(request):
    if request.method == "POST":
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        bouquet = CustomBouquet.objects.filter(session_key=session_key).first()

        if bouquet:
            CartItem.objects.create(
                user=request.user,
                custom_bouquet=bouquet,
                quantity=1
            )

    return redirect('cart')  # перекидываем в корзину после добавления


@csrf_exempt
def set_size(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        size = int(data.get('size', 0))
        if size in [15, 31, 51]:
            request.session['bouquet_size'] = size
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid size'}, status=400)
