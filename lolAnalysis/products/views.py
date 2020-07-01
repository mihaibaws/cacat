from .models import Product, Images
from .forms import ImageForm, ProductForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
								  DetailView,
								  UpdateView,
								  DeleteView)
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, RefundForm, PaymentForm
from django.conf import settings
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductListView(ListView):
	model = Product
	context_object_name  = 'model'
	template_name = 'products.html'
	

class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True


class ProductDeleteView(LoginRequiredMixin, DeleteView):
	model = Product
	success_url = '/'

#@login_required
def product_form_view(request):

    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra = 5)

    if request.method == 'POST':

        productForm = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())


        if productForm.is_valid() and formset.is_valid():
            product_form = productForm.save(commit=False)
            product_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(product=product_form, image=image)
                photo.save()
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/")
    else:
        productForm = ProductForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'products/addproduct.html',
                  {'product_form': productForm, 'formset': formset})
