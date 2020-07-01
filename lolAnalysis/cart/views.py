from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SizeForm, CheckoutForm, CouponForm, RefundForm, PaymentForm
from django.views.generic import ListView, DetailView, View
from django.http import HttpRequest
from Profile.models import UserProfile
from products.models import Product
from .serializers import OrderItemSerializaer
from django.core.mail import send_mail
from cart.models import OrderItem, Order, Payment, Coupon, Refund

import datetime
import stripe

import random
import string
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



def CheckoutView(request):
    form = CheckoutForm(request.POST)
    try:
        order = Order.objects.get(user=request.user,
                                  is_ordered=False)
        if form.is_valid():
            nume = form.cleaned_data.get(
                'nume')
            prenume = form.cleaned_data.get(
                'prenume')
            adresa = form.cleaned_data.get(
                'adresa')
            judet = form.cleaned_data.get(
                'judet')
            localitate = form.cleaned_data.get(
                'localitate')
            cod_postal = form.cleaned_data.get('cod_postal')
        else:
            nume, prenume, judet,  adresa, localitate, cod_postal = 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid'
        payment_option = form.cleaned_data.get('modalitate_de_plata')

        if payment_option == 'S':
            return redirect('payment', payment_option='stripe')
        elif payment_option == 'N':
            order_items = Order.objects.filter(user=request.user,
                                                is_ordered=False)[0]
            order_items.is_ordered = True
            for item in order_items.items.all():
                item.is_ordered = True
                item.save()
            order_items.nume = nume
            order_items.prenume = prenume
            order_items.adresa = adresa
            order_items.judet = judet
            order_items.localitate = localitate
            order_items.cod_postal = cod_postal
            order_items.ref_code = create_ref_code()
            order_items.save()

            date = f'{order_items.nume} {order_items.prenume} domiciliat la {order_items.judet}, {order_items.localitate}, {order_items.adresa}, a comandat produsele:'
            produse = ''
            for item in order_items.items.all():
                produse += f'{item},'
            message = f'{date} {produse}'
            send_mail(
                'Comanda',
                 message,
                 'mihaieugen233@yahoo.com',
                 ['paraschiva.silvia@yahoo.com'],
                 fail_silently= False,
            )
           

            messages.success(request, "Your order was successful!")
            return redirect('success-payment')
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("order-summary")
    return render(request, 'cart\checkout.html', {'order':order, 'form':form})

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'order': order,
        }   
        return render(self.request, "cart\payment.html", context)
       
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            try:
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="usd",
                    source=token
                )
                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(is_ordered=True)
                for item in order_items:
                    item.save()

                order.is_ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect('success-payment')

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/checkout/")


@login_required()
def success_payment(request):
    order_qs = Order.objects.filter(user=request.user, is_ordered=True)
    order = order_qs[0]
    context = {
        'order': order
    }
    return render(request, 'cart\success_payment.html', context)
    
@login_required()
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method =='POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data['size']
            order_item, created = OrderItem.objects.get_or_create(
                product=product,
                user=request.user,
                is_ordered=False,
                size=val
            )
    else:
        order_item = None
    print(request.POST) 
    
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug, size__iexact = order_item.size).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        print(order.items.all())
        print(order_item)
        order.items.add(order_item)
        print(order.items.all())
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def delete_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists(): 
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                is_ordered=False,
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products")


@login_required()
def order_details(request, **kwargs):
    try:
        order = Order.objects.get(user=request.user, is_ordered=False)
    except ObjectDoesNotExist:
        order = None
    context={
        'order':order
    }
    return render(request, 'cart/order_summary.html', context)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data['size']
    else:
        val = 'L'
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                is_ordered=False,
                size = val
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products")
