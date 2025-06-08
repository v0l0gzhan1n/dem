from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['full_name', 'email', 'phone', 'password']

    def __str__(self):
        return self.username

class Order(models.Model):
    ORDER_TYPE = (
        ('common', 'Общий клининг'),
        ('general', 'Генеральная уборка'),
        ('pastbuild', 'Послестроительная уборка'),
        ('chemical', 'Химчистка ковров'),
        ('furniture', 'Мебель'),
    )
    PAYMENT_TYPE = (
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    )
    STATUS_TYPE = (
        ('process', 'В работе'),
        ('confirm', 'Выполнено'),
        ('reject', 'Отменено'),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(max_length=255, choices=ORDER_TYPE)
    other = models.CharField(max_length=20, blank=True, null=True)
    comment_others = models.TextField(blank=True, null=True, default='Нет')
    payment_type = models.CharField(max_length=255, choices=PAYMENT_TYPE)
    status = models.CharField(max_length=255, choices=STATUS_TYPE, default='process')
    comment_by_admin = models.TextField(blank=True, null=True, default='Нет')

    def __str__(self):
        return self.customer.username

