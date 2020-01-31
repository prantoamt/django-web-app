from django.db import models

# Create your models here.
class Product(models.Model):
	types = (
		("featured", "Featured"),
		("on sale", "On Sale"),
		("new arrival", "New Arrival")
		)
	product_name = models.CharField(max_length=500, blank=False, null=False)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=30)
	sale = models.DecimalField(max_digits=100, decimal_places=2, default=30)
	stock = models.DecimalField(max_digits=100, decimal_places=2, default=30)
	category = models.CharField(max_length=400, choices=types, default="Featured")
	description = models.TextField(default="")
	slug = models.SlugField(default="")
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product_name
	class Meta:
		unique_together = ("product_name", "slug")	



class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete= models.CASCADE)
	image = models.ImageField(upload_to="products/images/", blank=True)
	featured = models.BooleanField(default=False)
	thumbnail = models.BooleanField(default=True)
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product.product_name