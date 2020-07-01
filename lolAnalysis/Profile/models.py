from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from products.models import Product
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, default = None, on_delete= models.CASCADE)
	nickname = models.CharField(max_length = 30,blank = False)
	division = models.CharField(max_length = 12,blank = True, default = "Unranked")
	division_img = models.ImageField(upload_to = "division_imgs", default ="UNRANKED.png")
	profile_img = models.ImageField(upload_to = "profile_imgs", default = "noob.png")
	product = models.ManyToManyField(Product, blank = True)
	stripe_id = models.CharField(max_length=200, null=True, blank=True)

	def create_profile(sender, instance, created, *args, **kwargs ):
		user_profile, created = UserProfile.objects.get_or_create(user = instance)
		if user_profile.stripe_id is None or user_profile.stripe_id == '':
			new_stripe_id = stripe.Customer.create(email=instance.email)
			user_profile.stripe_id = new_stripe_id['id']
			user_profile.save()


	post_save.connect(create_profile,sender=User)

	def __Str__(self):
		return self.user.username
		
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)