from django.db import models
from django.urls import reverse
from django.conf import settings
from django_countries.fields import CountryField


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50, blank = False)
    price = models.FloatField()
    description = models.TextField()
    thumbnail = models.ImageField(upload_to = 'product_img', blank = False)
    slug = models.SlugField()
    discount_price = models.FloatField()
    in_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })
        


class Images(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE, default = None)
	image = models.ImageField(upload_to = 'product_img', blank = True, null = True)

	def __str__ (self):
		return self.product.title
