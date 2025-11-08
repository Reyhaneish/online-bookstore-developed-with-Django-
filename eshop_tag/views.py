from django.shortcuts import render, get_object_or_404
from .models import Tag
from django.views.generic import DeleteView,ListView
from eshop_products.models import Product
# Create your views here.

# def tag_products(request, tag_id):
#     tag = get_object_or_404(Tag, id=tag_id)
#     products = tag.products.all()  # دریافت محصولات مرتبط با تگ
#     return render(request, 'tag/tag_products.html', {'tag': tag, 'products': products})
