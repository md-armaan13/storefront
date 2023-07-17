from rest_framework import serializers
from .models import Product, Reviews ,Cart ,CartItem, \
    Order ,OrderItem ,Address,Collection, Customer ,ProductImage
from .models import Collection
from decimal import Decimal
from django.db.models import F, Sum
from django.db import transaction



# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price_of_product = serializers.DecimalField(max_digits=6, decimal_places=2,source='price')
#     # custom field for api model
#     price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

#     def get_price_with_tax(self, object:Product):

#         return object.price *Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):
   # featured_product = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   # products_count = serializers.IntegerField(read_only=True)
    products_count_sample = serializers.SerializerMethodField(
        method_name='product_count', read_only=True)

    def product_count(self, object: Collection):
        return object.product_set.count()

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     annotated_value = instance.products_count
    #     data['products_count'] = annotated_value
    #     return data

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count_sample']


class sampleCollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(
        method_name='product_count')

    def product_count(self, object: Collection):
        return object.product_set.count()

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count', 'featured_product']
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']
    def create(self, validated_data):
        validated_data['product_id'] = self.context['product_id']
        return ProductImage.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    price_of_product = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='get_price_with_tax')
    collection_data = sampleCollectionSerializer(
        read_only=True, source='collection')
    productimage_set = ProductImageSerializer(many=True, read_only=True)
    def get_price_with_tax(self, object: Product):
        return object.price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price_of_product', 'price_with_tax',
                  'inventory', 'collection', 'description', 'collection_data','productimage_set']

    # def validate(self, attrs):
    #     if attrs['inventory'] < 0:
    #         raise serializers.ValidationError('inventory should be positive')
    #     return attrs
    def create(self, validated_data):
        product = Product(**validated_data)
        print(product)
        # product.description = 'dncioencwoj caipodcnl d'
        product.save()
        return product


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Reviews
        fields = ['id', 'date', 'name', 'description', 'rating','product']

        # def create(self, validated_data):
        #     product_id = self.context['product_id']
        #     print(product_id)
        #     review = Reviews.objects.create(product_id=product_id, **validated_data)

        # we can get product id in context object in serializer
           # return super().save(**self.validated_data)
    def create (self, validated_data):
        product_id = self.context['product_id']
        # review = Reviews.objects.create(product_id=product_id, **self.validated_data)
        validated_data['product_id'] = product_id
        return Reviews.objects.create(**validated_data)


class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory',]

class CartItemSerializer(serializers.ModelSerializer):
   # product = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductCartItemSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
    def create(self, validated_data):
       
        cart_id = self.context.get('cart_id')

        validated_data['cart_id'] = cart_id
        validated_data['product_id'] = self.context['request']['product_id']
       # print(validated_data)
        return CartItem.objects.create(**validated_data)
   
    def get_total_price(self, object: Cart):
        return object.quantity * object.product.price

    #since overiding save method as one cartcan only have unique product
    # if the product added alreadyexist in the cart we will update the quantity
    # else we will create new cartitem
    def save(self, **kwargs):
        try:
            cart_item = CartItem.objects.get(
            cart_id=self.context['cart_id'], product_id=self.context['request']['product_id'])
            #updating an existing item
            cart_item.quantity += self.validated_data['quantity']
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            #creating a new item
            self.instance= self.create(self.validated_data)
        return self.instance
    #methods for the validation individual fields'

    def validate(self, attrs):
        product_id = self.context['request']['product_id']
        if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError('product does not exist in the cart')
        return attrs

class UpdateCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = Cart
        fields = ['id','cartitem_set','total_price']
    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
    def get_total_price(self, object: Cart):
      return sum(item.quantity * item.product.price for item in object.cartitem_set.all())
      #return object.cartitem_set.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0


class CustomerSerializer(serializers.ModelSerializer):
    #user id is created dynamically so we need to define explicitly
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','membership','phone','birth_date','user_id']
    def create(self, validated_data):
        print(self.context)
        validated_data['user_id'] = self.context['user_id']
        customer = Customer.objects.create(**validated_data)
        return customer
   
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price']
   
class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True,read_only=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','orderitem_set']

    def save(self, **kwargs):
            # default payment status is pending

            with transaction.atomic():
                customer = Customer.objects.get(user_id=self.context['user_id'])
                order = Order.objects.create(customer_id= customer.id, payment_status='P') 

                cart_items = CartItem.objects.filter(cart_id=self.context['request']['cart_id'])
                order_item = [
                    OrderItem(
                        order_id=order.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        unit_price=item.product.price
                    ) for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_item)
                # it is sending empty response
                # cart_items.delete()
                order.refresh_from_db()
                return order
            
    def validate(self, attrs):
        if not Cart.objects.filter(pk=self.context['request']['cart_id']).exists():
            raise serializers.ValidationError('cart does not exist')
        elif CartItem.objects.filter(cart_id=self.context['request']['cart_id']).count()==0:
            raise serializers.ValidationError('cart is empty')
        return attrs

# THis serirlizer is to return the order id after placing the order
#because we are not returning the order id in the order serializer
# we are returning the order id in the response of the order view\
# so we need to create a new serializer

class ReturnOrderSerializer(serializers.ModelSerializer) :
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','orderitem_set']

    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']
    def create(self, validated_data):
        validated_data['product_id'] = self.context['product_id']
        return ProductImage.objects.create(**validated_data)