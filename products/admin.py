from django.contrib import admin
from .models import Product, ProductImage
from django.db import models


# Register your models here.
# Custom admin look for Products
class ProductAdmin(admin.ModelAdmin):
	# formfield_overrides = {
    #     models.TextField: {'widget': AdminPagedownWidget },
    # }
	date_hierarchy = 'timestamp'
	search_fields = ['product_name', 'description']
	list_display = ['product_name', 'price', 'sale', 'stock', 'active', 'updated']
	list_editable = ['price', 'sale', 'stock', 'active']
	list_filter = ['active', 'stock', 'price']
	readonly_fields = ['timestamp', 'updated']
	prepopulated_fields = {"slug":("product_name",)}
	class Meta:
		model = Product

# #Product image's custom look
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['product', 'featured', 'thumbnail', 'active', 'updated']
	list_editable = ['featured', 'thumbnail', 'active']
	class Meta:
		model = ProductImage

admin.site.register(Product, ProductAdmin) #Registers Products' Custom look to admin interface

admin.site.register(ProductImage, ProductImageAdmin)#Registers Product image's Custom look to admin interface