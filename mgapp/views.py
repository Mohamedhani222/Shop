from multiprocessing import context
from re import L, search
from unicodedata import category, name
from django.utils import timezone
from django.shortcuts import render , get_object_or_404 , redirect 
from django.contrib.auth.decorators import login_required
from .models import Category, Payment, Responseticket, Ticket, product,order,OrderDetails,User
from django.contrib import messages
import requests
from .filters import productFilter
from django.http import  JsonResponse
from django.db.models import Avg, Count, Min, Sum
from .forms import productsform,respform
import time
from django.core.mail import send_mail
from django.conf import settings
from .serializer import ProductSerializer
from rest_framework import generics



class getpro(generics.ListCreateAPIView):
    queryset=order.objects.all()
    serializer_class=ProductSerializer



########## Start AdminDashboard
@login_required(login_url='login')

def admindash(request):
    if request.user.is_staff:
        users = User.objects.all().order_by('id')
        usercount =users.count()
        productscount = product.objects.all().count()
        payments =Payment.objects.all().count()
        # lap = product.objects.filter(category='camera').count()
        ss =product.objects.annotate(x = Count("order__payment")).order_by('-x')[:2]
        zz =User.objects.all().annotate(s =Count("order__payment")).order_by("-s")[:5]
        ticketss =Ticket.objects.all()
        context={'productscount' : productscount , 
        'users':users,
        'usercount':usercount ,
        'orders':payments ,
        # 'lap':lap,
        "ss":ss ,
        'zz':zz,
        'tickets':ticketss
        }
        return render (request , 'Dashboard/admin.html' , context)
    return redirect("notfound")


def updateticket(request,id):
    if not Responseticket.objects.filter(ticket_id=id).exists():
        x= Ticket.objects.get(id=id)
        resp =Responseticket.objects.create(
            ticket =x,
            res =''
        )
        resp.save()
    ticket_id = Responseticket.objects.get(ticket_id=id)
    if request.method =='POST':

        form =respform(request.POST , instance=ticket_id)
        if form.is_valid():
            form.save()
            tic =Ticket.objects.get(id=ticket_id.ticket_id)
            tic.status ='closed'
            tic.save()
            return redirect('admin-dash')
    else:
        form =respform(instance=ticket_id)
        context={'form':form }

    if Ticket.objects.filter(id=id).exists():
        ticket =Ticket.objects.get(id=id)
        context={'form':form ,'ticket':ticket}

    return render (request , 'Dashboard/singleticket.html' , context)

##for user
def singleticket(request,id):

    tick =Ticket.objects.get( id=id , user=request.user)
    if Responseticket.objects.filter(ticket=tick.id).exists():
        res=Responseticket.objects.get(ticket=id )
        context={'ticket':tick , 'res':res}
    else:
        context={'ticket':tick }
    return render(request , 'ticketdetails.html' , context)

def tickets(request):
    if request.method =='POST':
        qs =request.POST['question']
        tkt =Ticket.objects.create(user=request.user,question =qs)
        tkt.save()
    tickets =Ticket.objects.filter(user=request.user)
    context ={
            'tickets':tickets
            }
    return render(request , 'tickets.html' , context)


#### For Ajax    
def adajx(request):
    payments =Payment.objects.all().count()
    data ={'payments' : payments}
    return JsonResponse(data)





@login_required(login_url='login')
def adminproducts(request ):
    if request.user.is_staff and not request.user.is_anonymous :
        productss = product.objects.all().order_by("id")
        products = product.objects.all().count()
        if request.method == 'POST':
            addpro = productsform(request.POST , request.FILES)
            if addpro.is_valid():
                addpro.save()
                messages.success(request , "تمت اضافة المنتج ")
                return redirect("admin-products")
        return render(request , 'Dashboard/products.html' , {'add':productsform , 'countpro':products , "products":productss })
    return redirect("notfound")

def adminproductdelete(request , id):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_staff:
        pro = get_object_or_404(product , id=id)
        pro.delete()
        return redirect('admin-products')

def customers(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_staff:
        users = User.objects.all().order_by("id")
        usercount =users.count()

        return render (request , "Dashboard/customers.html" , {'users':users ,"count":usercount})
    return redirect("notfound")

def delcust(request , id):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_staff:
        delcust =get_object_or_404(User , id=id)
        delcust.delete()
        return redirect("customers")
def customer(request , cs_id):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_staff:
        customer = User.objects.get(id=cs_id)
        orders = order.objects.filter(user =customer )
        return render(request , "Dashboard/customer.html" , {'customer':customer, 'orders':orders})
    return redirect("notfound")

def fil(request , id):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_staff:
        ordetails = OrderDetails.objects.all().filter(order_id = id)
        counterr =ordetails.count()
        return render(request , "Dashboard/order.html" , {  'ordetails':ordetails , 'order_id' : id , 'counterr':counterr })
    return redirect("notfound")

############### End AdminDashboard
def index(request):
    ss =product.objects.annotate(x = Count("order__payment")).order_by('-x')[:8]
    if request.method == 'POST':
        name = request.POST.get('nameperson')
        email = request.POST.get('email')
        message = request.POST.get('message')
    
        send_mail(
            f'message from {email}',
            "From " , name ,"email is", email ,"message is ", message   ,
            settings.EMAIL_HOST_USER,
            ['mohamedhani2003287@gmail.com'],
            fail_silently=False,
        )
        messages.success(request ,"Thanks For Contact With US ❤ ")

    context = {
        'ss' : ss,

    }
    return render(request ,'hh.html' ,context)

def userdash(request):
    products = product.objects.all()
    category =Category.objects.all()

    filter = productFilter(request.GET, queryset=products)
    products =filter.qs
    context ={'products' : products ,'filter': filter , 'category':category}
    if request.user.is_authenticated and not request.user.is_anonymous:
        if order.objects.all().filter(user = request.user , is_finished =False ):
            Order = order.objects.get(user = request.user , is_finished =False)
            orderdetails=OrderDetails.objects.all().filter(order=Order)
            counter =orderdetails.count()
            context={'products' : products ,'counter':counter ,'filter': filter ,'category':category}
    return render (request , 'index.html' , context)









def product_details(request ,id ):
    products_detail = get_object_or_404(product , id=id)
    context ={'products_detail' : products_detail }
    if request.user.is_authenticated and not request.user.is_anonymous:
        if order.objects.all().filter(user = request.user , is_finished =False ):
            Order = order.objects.get(user = request.user , is_finished =False)
            orderdetails=OrderDetails.objects.all().filter(order=Order)
            counter =orderdetails.count()
            context={'products_detail' : products_detail ,'counter':counter}
    return render (request , 'product.html' , context)




def notfound(request):
    return render(request , '404.html')

def addtocart(request ):
    if 'pro_id' in request.GET and 'price' in request.GET and 'qty' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        norder = order.objects.all().filter(user=request.user , is_finished = False)
        if not product.objects.all().filter(id =pro_id).exists():
            return redirect('notfound')

        pro = product.objects.get(id = pro_id)
        if norder :
            oldorder = order.objects.get(user = request.user , is_finished = False)
            orderdetails =OrderDetails.objects.create(
                product = pro,
                order = oldorder,
                price =pro.pirce ,
                quantity =qty

            )
            messages.success(request , "added for cart with old order")
            return redirect("/product/" + request.GET['pro_id'])

        else:
            messages.success(request , 'Done add to cart')
            new_order = order()
            new_order.user =request.user
            new_order.orderdate =timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(
                product = pro,
                order = new_order,
                price =pro.pirce ,
                quantity =qty
            )
            return redirect("/product/" + request.GET['pro_id'])
    else:
        return redirect ('login')

def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if order.objects.all().filter(user = request.user , is_finished =False ):
            Order = order.objects.get(user = request.user , is_finished =False)
            orderdetails=OrderDetails.objects.all().filter(order=Order)
            counter =orderdetails.count()
            total = 0
            for sum in orderdetails:
                total += sum.price * sum.quantity
            context ={
                'total':total,
                'orderdetails' :orderdetails ,
                'order': Order ,
                'counter':counter

              }

    return render (request , 'cart.html' , context)


def delete(request , orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        cart_del=OrderDetails.objects.get(id=orderdetails_id )
        if cart_del.order.user.id == request.user.id:
            cart_del.delete()
            return redirect('cart')
        else:
            return redirect("notfound")


def add_qty(request , id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        up_card = OrderDetails.objects.get(id=id)
        up_card.quantity += 1
        up_card.save()
        return redirect('cart')

def sub_qty(request , id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        up_card = OrderDetails.objects.get(id=id)
        if up_card.quantity > 1:
            up_card.quantity -= 1
            up_card.save()
            return redirect('cart')
        else:
            return redirect('cart')



def payment(request):
    context = None
    response =requests.get('http://ip-api.com/json')
    ip = response.json()
    if request.method == 'POST' and 'btn-payment' in request.POST and 'fname' in request.POST and 'lname' in request.POST and 'email' in request.POST and 'address' in request.POST and 'address2' in request.POST and 'ccname' in request.POST and 'ccnumber' in request.POST and 'expire' in request.POST and 'cvv' in request.POST and 'country' in request.POST and request.user.is_authenticated and not request.user.is_anonymous :

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        address2 = request.POST['address2']
        ccname = request.POST['ccname']
        ccnumber = request.POST['ccnumber']
        expire = request.POST['expire']
        cvv = request.POST['cvv']
        country =request.POST['country']
        Order = order.objects.get(user = request.user , is_finished =False)
        payment1 =Payment.objects.create(
            order =Order,
            fname =fname,
            lname=lname,
            email= email,
            address = address,
            address2 =address2,
            country = country,
            nameoncard =ccname,
            cardnumber =ccnumber,
            expiration =expire,
            cvv =cvv
        )
        payment1.save()
        Order.is_finished = True
        Order.save()
        return redirect("index")
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if order.objects.all().filter(user = request.user , is_finished =False ):
                Order = order.objects.get(user = request.user , is_finished =False)
                orderdetails=OrderDetails.objects.all().filter(order=Order)
                counter =orderdetails.count()
                total = 0
                for sum in orderdetails:
                    total += sum.price * sum.quantity
                context ={
                    'total':total,
                    'orderdetails' :orderdetails ,
                    'order': Order ,
                    'counter':counter,
                    'ip' :ip
                }

    return render (request , 'payment.html' , context)

def confirmorder(request):
    context =None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders =order.objects.all().filter(user = request.user , is_finished =True)
        if all_orders:
            for x in all_orders:
                Order = order.objects.get(id = x.id)
                orderdetails = OrderDetails.objects.all().filter(order=Order)
                counter =orderdetails.count()
                total = 0
                for sum in orderdetails:
                    total += sum.price * sum.quantity
                x.total =total
                x.counter =counter
    context ={
            'all_orders' : all_orders,
    }

    return render (request , 'confirm.html', context)




def addtocart2(request ):
    if 'pro_id' in request.GET and 'price' in request.GET and 'qty' in request.GET and request.user.is_authenticated and not request.user.is_anonymous :
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        norder = order.objects.all().filter(user=request.user , is_finished = False)
        if not product.objects.all().filter(id =pro_id).exists():
            return redirect('notfound')

        pro = product.objects.get(id = pro_id)
        if norder :
            oldorder = order.objects.get(user = request.user , is_finished = False)
            orderdetails =OrderDetails.objects.create(
                product = pro,
                order = oldorder,
                price =pro.pirce ,
                quantity =qty

            )
            return redirect("index")
        else:
            new_order = order()
            new_order.user =request.user
            new_order.orderdate =timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(
                product = pro,
                order = new_order,
                price =pro.pirce ,
                quantity =qty
            )
            return redirect("index")
    else:
        return redirect("login")



#tickets System

