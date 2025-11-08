"""
URL configuration for reyhaneeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import homepage,header,footer,ProductCategoryPartial,about_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('eshop_account.urls',namespace='account')),
    path('',include('eshop_order.urls',namespace='order')),
    path('',include('eshop_products.urls',namespace='products')),
    path('',include('eshop_contact.urls',namespace='eshop_contact')),
    path('',include('eshop_tag.urls',namespace='tags')),
    path('',homepage,name='home'),
    path('about/',about_page,name='about'),
    path('header/',header,name='header'),
    path('footer/',footer,name='footer'),
    path('products_category_partial', ProductCategoryPartial, name='products_category_partial'),
]

if settings.DEBUG:  # debug=True
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media  static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
