from typing import Any, List, Optional, Tuple
from django.contrib import admin ,messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from django.db.models import ExpressionWrapper
from django.db.models import IntegerField
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
# import  genric tabularInline

# Register your models here.

from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    #fields to be displayed on a filter
    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return  [
            ('lessthan','Low')
                ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() =='lessthan' :
           return queryset.filter(inventory__lt=10) 

  
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['inventory_action']
    # to display fields in admin panel
    list_display = ('title','price','inventory_status','collection_title','order_count')
   # to make fields editable
    list_editable = ['price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    autocomplete_fields = ['collection']
    search_fields   = ['title__istartswith']

    # method for collection field
    def collection_title(self,product)->str:
        return product.collection.title
    
    @admin.display(ordering='inventory')#`admin.display` decorator to specify the field to use for sorting
    def inventory_status(self,product)->str:
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'
        
    @admin.action(description='Clear inventory')#`admin.action` decorator to specify the description of the action
    def inventory_action(self,request,queryset):
        query_count=queryset.update(inventory=0)# returns number of rows updated

        self.message_user(request,f'{query_count} products were successfully updated',messages.SUCCESS)
    @admin.display(ordering='orders_count')
    def order_count(self,product):
        url = (reverse('admin:store_order_changelist')+'?'+
               urlencode({'product__id':str(product.id)}))
        return format_html('<a href="{}">{}</a>',url,product.orders_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders_count = Count('orderitem'))

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','membership','orders_count')
    list_select_related = ['user']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith']
    autocomplete_fields = ['user']

    #sending count of orders with link to orders page of that collection
    def orders_count(self,customer):
        url = (reverse('admin:store_order_changelist')+'?'+
               urlencode({'customer__id':str(customer.id)}))
        return format_html('<a href="{}">{}</a>',url,customer.orders_count)
        
    

    #modifying  base queryset
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders_count = Count('order'))


#Adding many to one relation to order
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','placed_at','payment_status','customer')
    list_editable = ['payment_status']
    list_per_page = 10
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    #list_select_related = ['customer']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title','products_count','new_products_count')
    list_per_page = 10
    search_fields = ['title__istartswith']

    def products_count(self,collection):
        url = (reverse('admin:store_product_changelist')+'?'+
               urlencode({'collection__id':str(collection.id)}))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)

    
    def new_products_count(self,collection)->int:
        return collection.new_products_count

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        expression = ExpressionWrapper(Count('product')*20,output_field=IntegerField())
        return super().get_queryset(request).prefetch_related('product_set').annotate(products_count = Count('product'),new_products_count = expression)
    #

class ProductInline(admin.TabularInline):
    model = models.Product.promotions.through
    extra = 1
    autocomplete_fields = ['product']


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('description','discount','products_count')
    list_per_page = 10
    search_fields = ['description__istartswith']
    inlines = [ProductInline]

    @admin.display(ordering='products_count')
    def products_count(self,promotion):
        url = (reverse('admin:store_product_changelist')+'?'+
                urlencode({'promotions__id':str(promotion.id)}))
        return format_html('<a href="{}">{}</a>',url,promotion.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count = Count('product'))
    
    

   