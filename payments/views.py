import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from payments.models import Item


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
class HomePageView(TemplateView):
    template_name = 'home.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(Item, id=pk)
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            'description': product.description,
                            'images': ['https://example.com/t-shirt.png'],
                        },
                    },
                    'quantity': 1,
                }]
            )
            print(checkout_session['id'])
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})

def show_selected_item(request, pk):
    item = Item.objects.get(id=pk)
    context={'item': item}
    return render(request, "item_detail.html", context)

