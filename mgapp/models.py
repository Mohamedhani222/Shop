from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django_countries.fields import CountryField
from creditcards.models import CardNumberField , CardExpiryField , SecurityCodeField
# Create your models here.


class Category(models.Model):
    category_name =models.CharField( max_length=250)
    def __str__(self) -> str:
        return self.category_name





class product(models.Model):
    title =models.CharField(max_length=200)
    description =models.TextField(max_length=10000 ,blank=True , null=True )
    oldprice =  models.IntegerField(blank=True , null=True)
    pirce = models.IntegerField()
    createdat = models.DateField(default=datetime.now() )
    image =models.ImageField(upload_to = 'photos')
    category = models.ForeignKey(Category , on_delete=models.SET_NULL, null =True , blank= True)

    def __str__(self) -> str:
        return self.title
    class Meta :
        ordering =['-createdat']
# Create your models here.

class order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    orderdate = models.DateTimeField(default=datetime.now())
    is_finished =models.BooleanField()
    details =models.ManyToManyField(product , through='OrderDetails')
    m=[('pending','pending' ) ,( 'Deliverd' , 'Deliverd'),('Out for delivery', 'Out for delivery') , ('Canceled' , 'Canceled')]
    status =models.CharField(max_length=100 , choices=m , default='pending')
    total = 0
    counter = 0
    def __str__(self) -> str:
        return str(self.id) 


class OrderDetails(models.Model):
    product = models.ForeignKey(product , on_delete=models.CASCADE)
    order = models.ForeignKey(order , on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6 , decimal_places=2)

    def __str__(self) -> str:
        return  str(self.product)



class Payment(models.Model):
    order = models.ForeignKey(order , on_delete=models.CASCADE)
    date =models.DateTimeField(default=datetime.now() , null=True , blank=True)
    fname= models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(null=True , blank=True)
    address =models.CharField(max_length=250)
    address2 =models.CharField(max_length=250 , null=True , blank=True)
    country =models.CharField(max_length=250 , null=True , blank=True)
    nameoncard = models.CharField(max_length=250)
    cardnumber = CardNumberField()
    expiration = CardExpiryField()
    cvv = SecurityCodeField()
    def __str__(self) -> str:
        return "User  " "  :  "  + str(self.order.user) + "  ( " + str(self.order.id) + " ) "


class Ticket(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    question =models.TextField(max_length=2000)
    createdat =models.DateTimeField(auto_now=True)
    choices =[('closed','closed' ), ('pending','pending'),('answerd','answerd')]
    status = models.CharField(max_length=200 ,choices=choices,default='pending')
    def __str__(self) -> str:
        return str(self.id)


class Responseticket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    res =models.TextField(max_length=2000 , null=True ,blank=True,default='')

    def __str__(self) -> str:
        return str(self.id)





