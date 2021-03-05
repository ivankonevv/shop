from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

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

class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Diagonal")
    display_type = models.CharField(max_length=255, verbose_name="Display "
                                                                 "type")
    processor_freq = models.CharField(max_length=255,
                                      verbose_name="Processor freq")
    ram = models.CharField(max_length=255, verbose_name="Ram")
    video = models.CharField(max_length=255, verbose_name="Graphics card")
    time_without_charge = models.CharField(max_length=255,
                                           verbose_name="Battery life")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Diagonal")
    display_type = models.CharField(max_length=255,
                                    verbose_name="Display type")
    resolution = models.CharField(max_length=255, verbose_name="Resolution")
    accum_volume = models.CharField(max_length=255,
                                    verbose_name="Accum volume")
    ram = models.CharField(max_length=255, verbose_name="Ram")
    sd = models.BooleanField(default=True)
    sd_volume = models.CharField(max_length=255, verbose_name="SD volume")
    main_cam_mp = models.CharField(max_length=255,
                                   verbose_name="Main cam max resolution")
    frontal_cam_mp = models.CharField(max_length=255,
                                      verbose_name="Frontal cam max resolution")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):
    user = models.ForeignKey("Customer", verbose_name="Customer",
                             on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart",
                             on_delete=models.CASCADE,
                             related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name="Final price")

    def __str__(self):
        return "Product: {}".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey("Customer", verbose_name="Customer",
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True,
                                      related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name="Final price")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Phone")
    address = models.CharField(max_length=255, verbose_name="Address")

    def __str__(self):
        return "Customer: {} {}".format(self.user.first_name,
                                        self.user.last_name)


