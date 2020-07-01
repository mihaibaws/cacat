from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from cart.models import Order

#from products.models import Order

# Create your views here.
@login_required
def Profile_view(request):
	my_user_profile = UserProfile.objects.filter(user = request.user).first()
	my_orders = Order.objects.filter(user=request.user)
	context = {
		'my_user_profile':my_user_profile,
		'my_orders':my_orders
	}
	
	return render(request, 'Profile/profile.html', context)
