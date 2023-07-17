import pprint
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
#impoert exceptionhandler from rest framework
from rest_framework.viewsets import ModelViewSet
#import createmodel mixin
from rest_framework.mixins import CreateModelMixin ,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.decorators import action
#import genericApiView
from rest_framework.generics import GenericAPIView
#import GenericViewSet
from rest_framework.viewsets import GenericViewSet
#import CreateAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.views import exception_handler
from django.db.models import Count

from .models import Order, Product,Reviews , Cart ,CartItem ,Customer ,ProductImage
from .serializers import OrderSerializer, ProductSerializer ,\
      CollectionSerializer ,ReviewSerializer , CartSerializer ,CartItemSerializer ,\
    UpdateCartItemSerializer ,CustomerSerializer , ReturnOrderSerializer ,ProductImageSerializer
from rest_framework import status
from .models import Collection
from .filters import ProductFilter
#impoet search filter
from rest_framework.filters import SearchFilter,OrderingFilter
#import isauthenticated
from rest_framework.permissions import IsAuthenticated ,IsAuthenticatedOrReadOnly,IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
# USING VIEWSET FOR THE SAME THING

from .permissions import IsAdminOrReadOnly


class ProductViewSet(ModelViewSet):
    # In our code i can not use this we have different query
    #to get, create and update the product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id']
    # def get_serializer_context(self):
    #     return {'request': self.request}

    def delete(self, request,  pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product cannot be deleted because it is associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


#class based views
class ProductList(ListCreateAPIView):

    queryset = Product.objects.select_related('collection').prefetch_related('collection__product_set','productimage_set').all().order_by('-last_update')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'price']

    #permission_classes = [IsAdminOrReadOnly]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]


    #CUSTOM FILTERING
    # def get_queryset(self):
    #     queryset =Product.objects.select_related('collection').prefetch_related('collection__product_set').all().order_by('-last_update')
    #     collection_id = self.request.query_params.get('collection_id')

    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset


#   OTHER METHOD TO DO THE SAME THING
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').prefetch_related('collection__product_set').all().order_by('-last_update')
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}



#   USING APIVIEW FOR THE SAME THING
    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').prefetch_related('collection__product_set').all().order_by('-last_update')
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         print("hello")
    #         handled_exception = exception_handler(e, None)
    #         if handled_exception is not None:
    #             return handled_exception
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductDetail(RetrieveUpdateDestroyAPIView) :
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#OVERIDING THE DELETE METHOD

    def delete(self, request,  pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product cannot be deleted because it is associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]
#   OTHER METHOD TO DO THE SAME THING
    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.prefetch_related('product_set').annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.prefetch_related('product_set').annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]

    def delete(self, request,  pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response({"error": "Collection cannot be deleted because it is associated with a product"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_serializer_context(self):
        print(self.kwargs)
        return {'product_id': self.kwargs['pk']}
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['pk'])
    # def perform_create(self, serializer):
    #     product_id = self.kwargs['pk']
    #     serializer.save(product_id=product_id)

class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_pk'


class CartList(CreateModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request):
        return self.create(request)
    

class CartDetail(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = CartSerializer
    
class CartItemList(ListCreateAPIView):
   # queryset = CartItem.objects.prefetch_related('product').all()
    serializer_class = CartItemSerializer
    def get_queryset(self):
       return CartItem.objects.prefetch_related('product').filter(cart_id=self.kwargs['pk'])

    def get_serializer_context(self):
        print(self.request.data)
        return {'cart_id': self.kwargs['pk'],
                'request': self.request.data}

class CartItemDetail(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete']
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return super().get_queryset().filter(cart_id=self.kwargs['cart_pk'])
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
        


class CustomerList(CreateModelMixin,GenericAPIView):
    queryset = Customer.objects.all() 
    serializer_class = CustomerSerializer
    permission_classes = []
    
   
   
    def get_serializer_context(self):
        print(self.request.user.id)
        return {'user_id': self.request.user.id}

    def post(self, request):
        return super().create(request)
     

class CustomerDetail(RetrieveModelMixin, GenericAPIView, UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = []

    #custom permission
    # def get_permissions(self):

    #     if self.request.method == 'GET':
    #         return [IsAuthenticated()]
    #     else:
    #         return [IsAdminUser()]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            customer = Customer.objects.get(user_id=user_id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Customer does not exist"})
        # return Response({
        #     "id" :request.user.id
        #     })
    def put(self, request, *args, **kwargs):
        try :
            customer = Customer.objects.get(user_id=request.user.id)
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Customer does not exist"})

class OrderList(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id,
                'request': self.request.data}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('orderitem_set').all()
        else:
            customer_id =  Customer.objects.get(user_id=self.request.user.id).id
            return Order.objects.prefetch_related('orderitem_set').filter(customer_id=customer_id)
   
   # modifying because current serilizer has fields which are read only
    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data ,context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order_serializer = ReturnOrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    

class OrderDetail(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('orderitem_set').all()
        else:
            customer_id =  Customer.objects.get(user_id=self.request.user.id).id
            return Order.objects.prefetch_related('orderitem_set').filter(customer_id=customer_id)
        
class ProductImageList(ListCreateAPIView):

    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}












# FUNCTION BASED VIEWS
@api_view()
#this will request with response from django rest frame work
#`api_view` is a decorator from django rest framework which will convert the function to a view
def product_list(request):
    #`Response` is a type of `HttpResponse from django rest framework
    queryset = Product.objects.select_related('collection').prefetch_related('collection__product_set').all().order_by('-last_update')
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data ) 
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

                 #OR

    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data )

@api_view()
def collection_list(request):
  #  queryset = Collection.objects.prefetch_related('product_set').all()
    queryset = Collection.objects.prefetch_related('product_set').annotate(products_count=Count('product')).all()

   # print(queryset.featured_product)
    serializer = CollectionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    # serializer = ProductSerializer(data=request.data)
    # try:
       
    #     x = serializer.is_valid()
    #     print(x)
    #     if serializer.is_valid(raise_exception=True):
    #         print(serializer.validated_data)
    #         serializer.save()
    #         return Response(serializer.data)
    # except ValidationError as e:
    #     print("hello")
    #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
      

    # except serializer.validated_data.DoesNotExist as e:
    #     print("hello")
    #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # except Exception as e:
    #     print("hello")
    #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("hello")
        handled_exception = exception_handler(e, None)
        if handled_exception is not None:
            return handled_exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def collection_create(request):
    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("hello")
        handled_exception = exception_handler(e, None)
        if handled_exception is not None:
            return handled_exception
        
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['PUT'])
def product_update(request, id):
    product = get_object_or_404(Product, pk=id)

    # you need send the instance of the product to the serializer and provide the data to update
    serializer = ProductSerializer(product,data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("hello")
        handled_exception = exception_handler(e, None)
        if handled_exception is not None:
            return handled_exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def review_create(request,pk):
    context = {'product_id': pk}
    print(context)
    serializer = ReviewSerializer(data=request.data,context=context)
    print(serializer)

    print(serializer.is_valid())
    serializer.is_valid(raise_exception=True)
    if serializer.is_valid():
        print(serializer.validated_data)
        review= serializer.save()
        print(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # try:
    #     print("hello4")
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # except Exception as e:
    #     print("hello")
    #     print(e)
    #     handled_exception = exception_handler(e, None)
    #     if handled_exception is not None:
    #         return handled_exception
    #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    