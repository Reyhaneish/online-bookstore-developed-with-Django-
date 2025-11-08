from django.shortcuts import render, redirect
from django.views.generic import ListView
from eshop_products.models import ProductCategory, Product
from eshop_sliders.models import Slider
from eshop_settings.models import SiteSettings
import itertools


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def homepage(request):
    sliders = Slider.objects.all()
    most_visited_products = Product.objects.order_by('-visit_count')[:8]
    latest_products = Product.objects.order_by('-id')[:8]
    featured_products = Product.objects.filter(is_featured=True)[:8]
    categories = ProductCategory.objects.prefetch_related('products').all()

    # ایجاد شناسه‌ها برای اسلایدها
    slider_ids = [f'section{i + 1}' for i in range(len(sliders))]  # ایجاد شناسه‌ها به صورت section1, section2, ...

    # افزودن شناسه‌ها به اسلایدها
    for i, slider in enumerate(sliders):
        slider.id = slider_ids[i]  # افزودن شناسه به هر اسلاید

    context = {
        'sliders': sliders,
        'featured_products': my_grouper(4, featured_products),
        'most_visited': my_grouper(4, most_visited_products),
        'latest_products': my_grouper(4, latest_products),
        'categories': categories
    }

    return render(request, 'home.html', context)


def header(request, *args, **kwargs):
    setting = SiteSettings.objects.get(id=1)
    context1 = {
        'settings': setting
    }
    return render(request, 'shared/Header.html', context1)


def footer(request, *args, **kwargs):
    site_setting = SiteSettings.objects.first()
    context2 = {
        'setting': site_setting
    }
    return render(request, 'shared/footer.html', context2)


def ProductCategoryPartial(request):
    categories = ProductCategory.objects.all()
    context3 = {'categories': categories}
    return render(request, 'products/product_categories_partial.html', context3)


def about_page(request):
    site_setting = SiteSettings.objects.get(id=1)
    context = {'setting': site_setting}
    return render(request, 'about_page.html', context)
