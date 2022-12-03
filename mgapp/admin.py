from distutils.log import info
from django.contrib import admin
from .models import Payment, Responseticket, Ticket,  product ,Category ,order,OrderDetails
# Register your models here.
admin.site.register(product)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(Responseticket)
class OrderDetailsAdmin(admin.ModelAdmin):
    model =OrderDetails

    list_display =['get_user','get_id','product' , 'quantity' ,'price']
    search_fields = ['order__id']
    list_filter= ['order__user']
    def get_id(self, obj):
        return obj.order.id
    get_id.admin_order_field  = 'order'  #Allows column order sorting
    get_id.short_description = 'order id'  #Renames column head
    
    def get_user(self, obj):
        return obj.order.user
    get_user.admin_order_field  = 'order'  #Allows column order sorting
    get_user.short_description = 'User'  #Renames column head

admin.site.register(OrderDetails ,OrderDetailsAdmin)

class orderAdmin(admin.ModelAdmin):
    model =order
    list_display =['id','user','is_finished']
    ordering =["-id"]
admin.site.register(order ,orderAdmin)

