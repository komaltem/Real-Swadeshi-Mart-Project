from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from .middlewares.auth import auth_middleware
from .models import SellerRegistration, Product, CustomerRegistration, Category, Order, Reviews, CustLocation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


# Create your views here.


class index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('index')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        # request.session.get('cart').clear
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)  # select
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, "index.html", data)


def BecomeSeller(request):
    return render(request, "BecomeSeller.html")


class SelSignup(View):
    def get(self, request):
        return render(request, 'BecomeSeller.html')

    def post(self, request):
        postDATA = request.POST
        fname = postDATA['fname']
        lname = postDATA['lname']
        semail = postDATA['semail']
        spassword = postDATA['spassword']
        scpassword = postDATA['scpassword']
        saddress = postDATA['saddress']
        gender = postDATA['gender']
        scity = postDATA['scity']
        sstate = postDATA['sstate']
        spincode = postDATA['spincode']
        scountry = postDATA['scountry']
        scompany = postDATA['scompany']

        # validation
        valu = {
            'fname': fname,
            'lname': lname,
            'semail': semail,
            'saddress': saddress,
            'gender': gender,
            'scity': scity,
            'sstate': sstate,
            'spincode': spincode,
            'scountry': scountry,
            'scompany': scompany,
        }
        error_message = None
        t = SellerRegistration(fname=fname, lname=lname, semail=semail, spassword=spassword, scpassword=scpassword,
                               saddress=saddress,
                               gender=gender, scity=scity, sstate=sstate, spincode=spincode, scountry=scountry,
                               scompany=scompany)
        error_message = self.validateSeller(t)
        # saving
        if not error_message:
            t.spassword = make_password(t.spassword)
            t.registration()
            return render(request, 'SellerSignin.html')
        else:
            sample = {
                'error': error_message,
                'values': valu
            }
            return render(request, 'BecomeSeller.html', sample)

    def validateSeller(self, t):
        error_message = None;
        if not t.fname:
            error_message = "First Name Required !!"
        elif len(t.fname) < 4:
            error_message = "First name must be 4 char long or more"
        elif not t.lname:
            error_message = "Last Name Required !!"
        elif len(t.lname) < 4:
            error_message = "Last Name must be 4 char long or more"
        elif len(t.spassword) < 6:
            error_message = "Password must be 6 char long or more"
        elif len(t.scpassword) < 6:
            error_message = "Confirm Password must be 6 char long or more"
        elif not t.saddress:
            error_message = "Address is Required !!"
        elif len(t.saddress) < 4:
            error_message = "Address must be 4 char long or more"
        elif not t.gender:
            error_message = "Gender is Required !!"
        elif len(t.gender) < 4:
            error_message = "Gender  must be 4 char long or more"
        elif not t.scity:
            error_message = "City Name Required !!"
        elif len(t.scity) < 4:
            error_message = "City Name must be 4 char long or more"
        elif not t.sstate:
            error_message = "State Required !!"
        elif len(t.sstate) < 3:
            error_message = "State must be 3 char long or more"
        elif not t.spincode:
            error_message = "Pincode is Required !!"
        elif len(t.spincode) < 6:
            error_message = "Pincode must be 6 char long or more"
        elif not t.scountry:
            error_message = "Country  Required !!"
        elif len(t.scountry) < 4:
            error_message = "Country must be 4 char long or more"
        elif not t.scompany:
            error_message = "Company Name Required !!"
        elif len(t.scompany) < 4:
            error_message = "Company Name must be 4 char long or more"
        elif len(t.semail) < 5:
            error_message = "Email Address must be 5 char long or more"
        elif t.isExists():
            error_message = "Email Address Already Registered..."
        return error_message


class SellerSignin(View):
    def get(self, request):
        return render(request, "SellerSignin.html")

    def post(self, request):
        semail = request.POST.get('semail')
        spassword = request.POST.get('spassword')
        scpassword = request.POST.get('scpassword')
        t = SellerRegistration.get_t_by_email(semail)

        error_message = None
        if t:
            flag = check_password(spassword, t.spassword)
            if flag:
                request.session['t'] = t.id
                request.session['semail'] = t.semail
                return redirect('seller_dashboard')
            else:
                error_message = 'Email or Password Invalid !!'
        else:
            error_message = 'Email or Password Invalid !!'
            return render(request, "SellerSignin.html", {'error': error_message})


def seller_dashboard(request):
    if request.session.get('t') is not None:
        return render(request, "seller_dashboard.html")
    else:
        return render(request, "SellerSignin.html")


def sellogout(request):
    del request.session["t"]  # session end
    return redirect('SellerSignin')


def product_upload(request):
    if request.method == "POST":
        pname = request.POST['pname']
        pprice = request.POST['pprice']
        pdescription = request.POST['pdescription']
        ppassword = request.POST['ppassword']
        image = request.FILES['image']

        p = Product(pname=pname, pprice=pprice, pdescription=pdescription, ppassword=ppassword, image=image)
        p.save()

        return HttpResponse("Registartion successfully")
    else:
        return HttpResponse("Fail")


class Signup(View):
    def get(self, request):
        return render(request, 'sign_up.html')

    def post(self, request):
        postData = request.POST
        uname = postData['uname']
        uemail = postData['uemail']
        unumber = postData['unumber']
        upassword = postData['upassword']
        uconfirmpassword = postData['uconfirmpassword']

        # validation
        value = {
            'uname': uname,
            'uemail': uemail,
            'unumber': unumber,
        }

        error_message = None
        customer = CustomerRegistration(uname=uname, uemail=uemail, unumber=unumber, upassword=upassword,
                                        uconfirmpassword=uconfirmpassword)
        error_message = self.validateCustomer(customer)
        # saving
        if not error_message:
            customer.upassword = make_password(customer.upassword)
            customer.register()
            return render(request, 'user_dashboard.html')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'sign_up.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if not customer.uname:
            error_message = "Full Name Required !!"
        elif len(customer.uname) < 4:
            error_message = "Full name must be 4 char long or more"
        elif not customer.unumber:
            error_message = "Phone Number Required !!"
        elif len(customer.unumber) < 10:
            error_message = "Last Name must be 10 char long or more"
        elif len(customer.upassword) < 6:
            error_message = "Password must be 6 char long"
        elif len(customer.uconfirmpassword) < 6:
            error_message = "Confirm Password must be 6 char long"
        elif len(customer.uemail) < 5:
            error_message = "Email Address must be 5 char long"
        elif customer.isExists():
            error_message = "Email Address Already Registered..."

        return error_message


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "login.html")

    def post(self, request):
        uemail = request.POST.get('uemail')
        upassword = request.POST.get('upassword')
        uconfirmpassword = request.POST.get('uconfirmpassword')
        customer = CustomerRegistration.get_customer_by_email(uemail)

        error_message = None
        if customer:
            flag = check_password(upassword, customer.upassword)
            if flag:
                request.session['customer'] = customer.id
                request.session['customer'] = customer.uname
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                return redirect('user_dashboard')
            else:
                error_message = 'Email or Password Invalid !!'
        else:
            error_message = 'Email or Password Invalid !!'
            return render(request, "login.html", {'error': error_message})

def custlocation(request):
    if request.method == "POST":
      custaddress = request.POST['custaddress']
      custcity = request.POST['custcity']
      custpincode = request.POST['custpincode']

      cl = CustLocation(custaddress=custaddress, custcity=custcity, custpincode=custpincode)
      cl.save()

      return HttpResponse("done")
    else:
        return HttpResponse("fail")


class user_dashboard(View):
    def get(self, request):
        if request.session.get('customer') is not None:
            return render(request, "user_dashboard.html")
        else:
            return render(request, "login.html")


def logout(request):
    del request.session["customer"]  # session end
    return redirect('login')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})


class check_out(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=CustomerRegistration(id=customer), product=product, price=product.pprice,
                          address=address, phone=phone, quantity=cart.get(str(product.id)))

            order.save()
        request.session['cart'] = {}
        return redirect('cart')


class Orders(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


def edit_cust(request):
    profile = CustomerRegistration.objects.all()
    return render(request, "user_dashboard.html", {'profile': profile})


class cureview(View):
    def post(self, request):
        revimage = request.FILES.get('revimage')
        rname = request.POST.get('rname')
        customer = request.session.get('customer')
        creview = request.POST.get('creview')

        custreview = Reviews(customer=CustomerRegistration(id=customer), rname=rname, creview=creview,
                             revimage=revimage)
        custreview.save()


def wecome(request):
    return render(request, "wecome.html")


def reviews(request):
    return render(request, "Reviews.html")


def search(request):
   q= request.GET['q']
   products=Product.objects.filter(pname__icontains =q).order_by('-id')
   return render(request,'search.html', {'products':products})
