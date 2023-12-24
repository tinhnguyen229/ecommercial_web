from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class Category(models.Model):
    sub_category = models.ForeignKey(to='self',
                                     on_delete=models.CASCADE,
                                     related_name='sub_categories',
                                     null=True,
                                     blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    category = models.ManyToManyField(to=Category, related_name='product')
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        try:
            img_url = self.image.url
        except:
            img_url = ''
        return img_url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return 'order' + str(self.id)

    @property
    def get_total_order_item_quantity(self):
        order_items = self.orderitem_set.all()
        return sum([order_item.quantity for order_item in order_items])

    @property
    def get_total_order_item_price(self):
        order_items = self.orderitem_set.all()
        return sum([order_item.get_total_price for order_item in order_items])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address