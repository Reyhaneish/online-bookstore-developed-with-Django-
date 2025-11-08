import itertools

from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from eshop_order.forms import UserNewOrderForm
from .models import Product, ProductGallery
from eshop_product_category.models import ProductCategory
# from django.db.models import Q


# Create your views here.


class ProductList(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        return Product.product_manager.get_active_products()


class ProductListByCategory(ListView):
    template_name = 'products/product_list.html'
    paginate_by = 2

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        product_category = ProductCategory.objects.filter(name__exact=category_name).first()
        if product_category is None:
            raise Http404('صفحه یافت نشد')  # خروجی میده^^
        return Product.product_manager.get_products_by_category(category_name)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def ProductDetail(request, *args, **kwargs):
    selected_product_id = kwargs['id']
    user_order = UserNewOrderForm(request.POST or None, initial={'product_id': selected_product_id})
    product = Product.objects.get(id=selected_product_id)  # استفاده از objects.get به جای product_manager.get_by_id

    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    # product.visit_count+=1
    # product.save()
    if 'viewed_products' not in request.session:
        request.session['viewed_products'] = []

    if selected_product_id not in request.session['viewed_products']:
        product.visit_count += 1
        product.save()
        request.session['viewed_products'].append(selected_product_id)

    related_products = Product.objects.filter(category__in=product.category.all()).exclude(
        id=selected_product_id).distinct()

    # related_products = Product.objects.filter(category__product=product).exclude(
    #     id=selected_product_id).distinct()  # محصولات مرتبط
    group_related_products = my_grouper(3, related_products)  # محصولات مرتبط

    galleries = ProductGallery.objects.filter(product=product)  # استفاده از product به جای product_id
    grouped_galleries = list(my_grouper(2, galleries))  # items in groped_galleries variable is list

    context = {
        'product': product,
        'grouped_galleries': grouped_galleries,
        'related_products': group_related_products,
        'user_order': user_order
    }
    return render(request, 'products/product_detail.html', context)


class SearchProductView(ListView):
    template_name = 'products/product_list.html'
    model = Product
    context_object_name = 'product'
    paginate_by = 2

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')  # دریافت پارامتر جستجو از URL
        if query:  # اگر query وجود داشته باشد
            return Product.product_manager.search(query)  # جستجو در عنوان محصولات فعال
        return Product.objects.filter(active=True)  # اگر query وجود نداشته باشد، فقط محصولات فعال را برمی‌گرداند
