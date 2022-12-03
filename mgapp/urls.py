from django.urls import path
from . import views
urlpatterns = [
    path('products', views.userdash , name='index'),
    path('product/<int:id>' ,views.product_details , name='product'),
    path('addtocart/', views.addtocart , name='addtocart'),
    path('addtocart2/', views.addtocart2 , name='addtocart2'),
    path('404-not-found/', views.notfound , name='notfound'),
    path('cart', views.cart , name='cart'),
    path('delete/<int:orderdetails_id>', views.delete , name='delete'),
    path('add/<int:id>', views.add_qty , name='add'),
    path('sub/<int:id>', views.sub_qty , name='sub'),
    path('payment' , views.payment , name='payment'),
    path('orders' , views.confirmorder , name='orders'),
    path('' , views.index , name='home'),
    #### For admin Dashboard
    path('admin-dashboard', views.admindash , name='admin-dash'),
    path('admin-dashboard/products', views.adminproducts , name='admin-products'),
    path("del/<int:id>" , views.adminproductdelete , name="del"),
    path("block/<int:id>" , views.delcust , name="delcust"),
    path("customer/<int:cs_id>" , views.customer , name="customer"),
    path("order/<int:id>" , views.fil , name="order"),
    path("admin-dashboard/customers" , views.customers , name="customers"),
    path("ajax" , views.adajx , name="adajx"),
    path("pros" , views.getpro.as_view() , name="pros"),
    path("admin-dashboard/ticket/<int:id>" , views.updateticket , name="updateticket"),
    path("ticket/<int:id>" , views.singleticket , name="ticket"),
    path("tickets/" , views.tickets , name="tickets"),

]
