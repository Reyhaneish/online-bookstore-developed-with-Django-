from django.db import models
from django.contrib.auth.models import User
from eshop_products.models import Product


# Create your models here.
# CASCADE:زمانی که یک کاربر حذف بشه میاد سبد خرید مربوط بهش رو هم حذف میکنه

class Order(models.Model):  # مدل سبد خرید
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # این سبد خرید برای چه کسی است
    is_paid = models.BooleanField(verbose_name='پرداخت شده/نشده', null=True, blank=True)
    payment_date = models.DateTimeField(verbose_name='تاریخ پرداخت', null=True, blank=True)  # تاریخ و زمان پرداخت

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    def __str__(self):
        return self.owner.get_full_name()  # get_full_name:میاد کاربری که ساخته اسم و فامیلش رو
        #  میچسبونه به هم و نشون میده

    def get_order_details(self):
        return self.orderdetail_set.all()


#جزئیات سبد خرید
class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orderdetail_set',verbose_name='سبد خرید')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    price=models.IntegerField(verbose_name='قیمت محصول')
    count=models.IntegerField(verbose_name='تعداد')

    def get_detail_sum(self):
        return self.count * self.price

    class Meta:
        verbose_name='جزئیات محصول'
        verbose_name_plural='اطلاعات جزئیات محصولات'

    def __str__(self):
        return self.product.title