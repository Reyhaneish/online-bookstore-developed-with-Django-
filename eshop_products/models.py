import os
from django.db.models import Q
from django.db import models
from eshop_product_category.models import ProductCategory
from eshop_tag.models import Tag

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries{final_name}"


class ProductManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_by_id(self, id):  # برای دریافت محصول بر اساس شناسه
        try:
            return self.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get_queryset(self):
        return super().get_queryset()

    def search(self,query):
        lookup=Q(title__icontains=query)|Q(description__icontains=query)
        return self.filter(lookup, active=True).distinct()

    def get_products_by_category(self,category_name):
        return self.get_queryset().filter(category__name__exact=category_name,active=True)


# class ProductManager(models.Manager):
#     def get_active_products(self):
#         return self.get_queryset().filter(active=True)
#
#     def get_by_id(self,id):
#         qs = self.get_queryset().get(id=id)
#         if qs.count() == 1:
#             return qs.first()
#         else:
#             return None
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to=upload_gallery_image_path, null=True, blank=True, verbose_name='تصویر')
    author=models.CharField(max_length=200,verbose_name='نویسنده',null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    category=models.ManyToManyField(ProductCategory,related_name='products',blank=True,verbose_name='دسته بندی ها')
    tag=models.ManyToManyField(Tag,blank=True)
    visit_count=models.IntegerField(default=0,verbose_name='تعداد بازدید')
    is_featured=models.BooleanField(default=False,verbose_name='برگزیده')

    objects = models.Manager()
    product_manager = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}/"


class ProductGallery(models.Model):
    title=models.CharField(max_length=150,verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_gallery_image_path, null=True, blank=True, verbose_name='تصویر')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name='گالری تصویر'
        verbose_name_plural='گالری تصاویر'

    def __str__(self):
        return self.title
