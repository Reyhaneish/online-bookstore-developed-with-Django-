import os

from django.db import models


# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries{final_name}"


class SiteSettings(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    address = models.CharField(max_length=400, verbose_name='آدرس')
    phone = models.CharField(max_length=50, verbose_name='شماره تماس')
    email = models.CharField(max_length=50, verbose_name='ایمیل')
    fax = models.CharField(max_length=50, verbose_name='فکس')
    about_us = models.TextField(verbose_name='درباره ما', blank=True, null=True)
    copyright = models.CharField(verbose_name='متن کپی رایت', null=True, blank=True)
    logo = models.ImageField(upload_to=upload_gallery_image_path, null=True, blank=True, verbose_name='تصویر')
    header_logo=models.ImageField(upload_to=upload_gallery_image_path, null=True, blank=True, verbose_name='لوگو')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'مدیریت تنظیمات'

    def __str__(self):
        return self.title
