from django.shortcuts import render

#import htttprespone
from django.http import HttpResponse
from store.models import Product , OrderItem ,Order ,Customer ,Collection ,Promotion
# Create your views here.
# import q from django
from django.db.models import Q ,F
from django.db.models import Prefetch
from django.db.models import Count
#import contentype
from django.contrib.contenttypes.models import ContentType
# impoet tagitem
from tags.models import TaggedItem
from django.db import transaction

#import send_mail
from django.core.mail import send_mail,mail_admins,BadHeaderError
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
   
  #  product = Product.objects.prefetch_related('promotions').select_related('collection').all()
   # orders = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').all().order_by('-placed_at')[:5]
    #customer = Customer.objects.annotate(orders_count = Count('order')).filter(orders_count__gt = 0)


      #ACESSING REFRENCING FIELDS
      # {% for item in order.orderitem_set.all %}
      #           <li>
      #               <p>Order Item ID: {{ item.id }}</p>
      #               <p>Quantity: {{ item.quantity }}</p>
      #               <p>Unit Price: {{ item.unit_price }}</p>
      #               <p>Product: {{ item.product.title }}</p>
                    
      #           </li>
      #       {% endfor %}
    #  for item in order.orderitem_set.all():)
    #order_items = order.orderitem_set.all()
  #  print(order[0].orderitem_set.values_list('id'))


    #QUERING THE ASSOCIATED MODEL
    # content_type = ContentType.objects.get_for_model(Product)
    # tag_item = TaggedItem.objects.filter(content_type=content_type,object_id=1)
    # list(tag_item)
    # print(tag_item)
    

    #CREAATING AN OBJECT
    # product = Product()
    # product.title = 'apple - watch'
    # product.description = 'A next GenZ watch'
    # product.price = 100
    # product.inventory = 10
    # product.collection= Collection.objects.get(pk=9)
    # #add multiple promotion to the product as it is many to many field
    # product.save()
    # print(product)
    # promotion = Promotion.objects.filter(id__in=[1,2])
    # product.promotions.add(*promotion)  #The asterisk (*) before promotion is used for argument unpacking. It allows you to pass multiple objects as separate arguments

    
    #product.promotions.add(promotion1, promotion2)
   

   #UPDATING THE OBJECT
    # product = Product.objects.prefetch_related('promotions').select_related('collection').get(pk=1022)
    # product.description = 'A cult watch'
    # product.save()
    

    #USING TRANSACTION
    with transaction.atomic():
      order =Order()
      order.customer = Customer.objects.get(pk=1)
      order.payment_status = 'P'
      order.placed_at = '2020-01-01'

      order.save()

      order_item = OrderItem()
      order_item.product = Product.objects.get(pk=1)
      order_item.quantity = 2
      order_item.unit_price = 100
      order_item.order = order
      order_item.save()
     
   

    context = {
        'orders': [],
    } 
    return render(request, 'playground/index.html', context)


def send_email(request):
    try:
        #send_mail(subject='Subject here', message='Here is the message.',from_email= 'info@moshbuy.com',recipient_list=['arman.cool4080@gmail.com'])
       # send_mail('Subject here', 'Here is the message.','arman.cool4080@gmail.com',['arman.kanpur4080@gmail.com'])

      message = BaseEmailMessage(
        template_name='emails/index.html',
        context={
            'name': 'Armaan',
        },
      )
      message.attach_file('playground/static/Armaan photo.jpg')
      message.send(['arman.kanpur4080@gmail.com'])
      

    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponse('Email sent successfully')