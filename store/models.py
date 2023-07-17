from django.db import models

#import validators
from django.core.validators import MinValueValidator

#import settings
from django.conf import settings

from .validators import validate_file_size


# Create your models here.
from uuid import uuid4

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
    # this one to one or many to one relationship?
    # many to one

    # create an filed of an array of featured products


    #related_name is used to avoid defualt name (collection_set)
    #relatedname=+ means that we dont want to create reverse relationship

    # TO CHANGE THE DEFAULT REPRESENTATION OF A MODEL
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1,message='Price should be positive')]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0,message='Inventory should be positive')])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT)
    # Django will create reverse relationship with promotions
    promotions = models.ManyToManyField('Promotion',default=None, blank=True)
    # related name is used to avoid defualt name (product_set)
    # what is reverse lookup
    # https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    # image = models.ImageField(upload_to='product-images', blank=True)
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/images',validators=[validate_file_size])                            

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=20 ,null=True, blank=True)
    #what is blank= true means
    #https://stackoverflow.com/questions/8609192/django-model-field-default-and-blank-true
    birth_date = models.DateField(null=True)  # don not use datetimefield
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    # image = models.ImageField(upload_to='customer-images', blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
  
    def first_name(self):
        return self.user.first_name
  
    def last_name(self):
        return self.user.last_name
    

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # we should never delete our orders as it represent sales


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)
    # For one to one always use primary key
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, primary_key=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
  #  cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'cart']
# MAny To Many Relationship

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.description
    # product_set
    # django will create reverse relationship with products


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='reviews')
    # related_name is used to avoid defualt name (reviews_set)
    # related_name=+ means that we dont want to create reverse relationship
    # prod
    name = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)