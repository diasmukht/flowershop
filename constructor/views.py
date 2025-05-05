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

    total_flowers = 0
    if bouquet:
        total_flowers = sum(item.quantity for item in bouquet.custombouquetflower_set.all())

    html = render_to_string('constructor/_summary_mini.html', {
        'bouquet': bouquet,
        'total_flowers': total_flowers
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