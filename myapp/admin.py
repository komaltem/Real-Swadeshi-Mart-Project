from django.contrib import admin
from .models import SellerRegistration, Category, Product, CustomerRegistration, Order, Reviews, CustLocation


class AdminProduct(admin.ModelAdmin):
    list_display = ['pname', 'pprice', 'category']


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(SellerRegistration)
admin.site.register(CustomerRegistration)
admin.site.register(Order)
admin.site.register(Reviews)
admin.site.register(CustLocation)
