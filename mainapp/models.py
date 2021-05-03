from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Product name"
    )
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Image")
    description = models.TextField(verbose_name="Description", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name="Price")

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    user = models.ForeignKey("Customer", verbose_name="Customer",
                             on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart",
                             on_delete=models.CASCADE,
                             related_name="related_products")
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name="Final price")

    def __str__(self):
        return "Product: {}".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey("Customer", verbose_name="Customer",
                              null=True,
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True,
                                      related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      default=0,
                                      verbose_name="Final price")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="User",
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Phone", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Address", null=True, blank=True)
    orders = models.ManyToManyField('Order', blank=True, verbose_name='Customer orders', related_name='related_customer')

    def __str__(self):
        return "Customer: {} {}".format(self.user.first_name,
                                        self.user.last_name)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAYED = 'payed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Pickup'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    STATUS_CHOICES = (
        (STATUS_PAYED, 'Order has been paid'),
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order completed')
    )

    customer = models.ForeignKey(Customer, verbose_name='Customer', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    phone = models.CharField(max_length=255, verbose_name='Phone')
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Order status',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Order type',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Order comment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Created')
    order_date = models.DateField(verbose_name='Date of receipt of the order', default=timezone.now)

    def __str__(self):
        return str(self.id)
