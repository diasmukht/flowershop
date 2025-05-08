from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse, QueryDict
from decimal import Decimal
import json, requests
from users.models import Profile  # Добавь в импорты рядом с другими
from flowers.models import Bouquet, BouquetFlower
from main.models import CartItem
from constructor.models import CustomBouquet

def bouquet_detail(request, id):
    bouquet = get_object_or_404(Bouquet, id=id)
    composition = BouquetFlower.objects.filter(bouquet=bouquet).select_related('flower')
    return render(request, 'main/bouquet_detail.html', {'bouquet': bouquet, 'composition': composition})

def home(request):
    return render(request, 'main/home.html')

@login_required
def add_to_cart(request, id):
    bouquet = get_object_or_404(Bouquet, id=id)
    item, created = CartItem.objects.get_or_create(user=request.user, bouquet=bouquet, custom_bouquet=None)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('bouquet_detail', id=id)

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = Decimal('0.00')

    for item in items:
        total += item.get_price()

    # Упаковка (фиксированная стоимость, например 500 ₸)
    packaging_cost = Decimal('500.00')
    total += packaging_cost

    # Профиль пользователя
    profile = Profile.objects.get(user=request.user)
    discount = Decimal('0.00')
    delivery = Decimal('0.00')
    gift = False

    if profile.status == 'advanced':
        discount = total * Decimal('0.10')
        delivery = Decimal('1000.00')
    elif profile.status == 'vip':
        discount = total * Decimal('0.15')
        delivery = Decimal('0.00')  # Бесплатная доставка
        gift = True
    elif profile.status == 'regular':
        discount = 0
        delivery = Decimal('1000.00')
    total_with_discount = total - discount + delivery

    return render(request, 'main/cart.html', {
        'items': items,
        'total': total,
        'discount': discount,
        'delivery': delivery,
        'gift': gift,
        'total_with_discount': total_with_discount,
        'packaging_cost': packaging_cost,
        'profile': profile,
    })


@login_required
@require_POST
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')

@login_required
@require_POST
def checkout(request):
    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'main/checkout_success.html')

@csrf_exempt
def gpt_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            print("GROQ RAW RESPONSE:", response.text)
            response.raise_for_status()

            gpt_reply = response.json()['choices'][0]['message']['content']
            return JsonResponse({'response': gpt_reply})

        except Exception as e:
            print("GROQ API ERROR:", e)
            return JsonResponse({'error': 'GPT processing error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def catalog_view(request):
    bouquets = Bouquet.objects.filter(available=True)

    selected_flower_types = request.GET.getlist('flower_type')
    selected_size_types = request.GET.getlist('size')
    selected_decor_types = request.GET.getlist('decor')
    selected_vase_types = request.GET.getlist('vase')
    selected_delivery_dates = request.GET.getlist('delivery_date')
    manufacturer = request.GET.get('manufacturer')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if selected_flower_types:
        bouquets = bouquets.filter(flower_type__in=selected_flower_types)
    if selected_size_types:
        bouquets = bouquets.filter(size__in=selected_size_types)
    if selected_decor_types:
        bouquets = bouquets.filter(decor__in=selected_decor_types)
    if selected_vase_types:
        bouquets = bouquets.filter(vase__in=selected_vase_types)
    if selected_delivery_dates:
        bouquets = bouquets.filter(delivery_date__in=selected_delivery_dates)
    if manufacturer:
        bouquets = bouquets.filter(manufacturer=manufacturer)
    if request.GET.get('has_discount'):
        bouquets = bouquets.filter(has_discount=True)
    if price_min:
        bouquets = bouquets.filter(price__gte=Decimal(price_min))
    if price_max:
        bouquets = bouquets.filter(price__lte=Decimal(price_max))

    paginator = Paginator(bouquets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    if 'page' in querydict:
        del querydict['page']
    querystring = querydict.urlencode()

    for b in page_obj:
        if b.has_discount:
            b.discount_price = (b.price * Decimal('0.85')).quantize(Decimal('1.00'))

    context = {
        'page_obj': page_obj,
        'querystring': querystring,
        'flower_types': ['rose', 'lily', 'daisy', 'tulip'],
        'decor_types': ['ribbon', 'box', 'garland'],
        'vase_types': ['ceramic', 'glass'],
        'size_types': ['standard', 'deluxe', 'premium'],
        'selected_flower_types': selected_flower_types,
        'selected_size_types': selected_size_types,
        'selected_decor_types': selected_decor_types,
        'selected_vase_types': selected_vase_types,
        'selected_delivery_dates': selected_delivery_dates,
    }

    return render(request, 'main/catalog.html', context)

