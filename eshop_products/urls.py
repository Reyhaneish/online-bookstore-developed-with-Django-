from django.urls import path
from .views import (ProductList, ProductDetail, SearchProductView, ProductListByCategory,)


app_name = 'products'

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:id>/<title>/', ProductDetail, name='product_detail'),
    path('products/search/', SearchProductView.as_view(), name='product_search'),
    path('products/<category_name>/', ProductListByCategory.as_view(), name='product_category'),

]
