import datetime

from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    pname = models.CharField(max_length=50)
    pprice = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pdescription = models.CharField(max_length=200)
    ppassword = models.CharField(max_length=40)
    image = models.FileField(upload_to='media/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class CustomerRegistration(models.Model):
    uname = models.CharField(max_length=80)
    uemail = models.CharField(max_length=50, default="0")
    unumber = models.CharField(max_length=50)
    upassword = models.CharField(max_length=30, default="0")
    uconfirmpassword = models.CharField(max_length=30, default="0")

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(uemail):
        try:
            return CustomerRegistration.objects.get(uemail=uemail)
        except:
            return False

    def isExists(self):
        if CustomerRegistration.objects.filter(uemail=self.uemail):
            return True

        return False


class SellerRegistration(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    semail = models.CharField(max_length=70)
    spassword = models.CharField(max_length=30)
    scpassword = models.CharField(max_length=30)
    saddress = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)
    scity = models.CharField(max_length=50)
    sstate = models.CharField(max_length=50)
    spincode = models.CharField(max_length=20)
    scountry = models.CharField(max_length=50)
    scompany = models.CharField(max_length=100)

    def isExists(self):
        if SellerRegistration.objects.filter(semail=self.semail):
            return True

        return False

    def registration(self):
        self.save()

    @staticmethod
    def get_t_by_email(semail):
        try:
            return SellerRegistration.objects.get(semail=semail)
        except:
            return False


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order \
            .objects \
            .filter(customer=customer_id) \
            .order_by('-date')


class Reviews(models.Model):
    customer = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    rname = models.CharField(max_length=200)
    creview = models.CharField(max_length=500)
    revimage = models.FileField(upload_to='Reviewimg')


class CustLocation(models.Model):
    custaddress = models.CharField(max_length=200)
    custcity = models.CharField(max_length=50)
    custpincode = models.CharField(max_length=10)

