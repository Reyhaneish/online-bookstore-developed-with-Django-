# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from eshop_products.models import Product
from .forms import UserNewOrderForm
from .models import Order, OrderDetail


class AddUserOrderView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        user_order = UserNewOrderForm(request.POST)
        if user_order.is_valid():
            order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
            if order is None:
                order = Order.objects.create(owner_id=request.user.id, is_paid=False)

            product_id = user_order.cleaned_data.get('product_id')
            count = user_order.cleaned_data.get('count')
            if count < 0:
                count = 1

            product = Product.product_manager.get_by_id(product_id)
            order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)
            # todo: redirect user to user panel
            # return redirect('/user/orders)
            return redirect(f'/products/{product.id}/{product.title.replace(" ", "-")}')
        return redirect('/')


# request.user.id => دسترسی به آیدی کاربری که لاگین کرده است
@login_required(login_url='/login')
def user_open_order(request):
    context = {
        'order': None,
        'details': None,
        'total': 0,
    }
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()

        # محاسبه جمع کل قیمت محصولات
        total = sum(detail.product.price * detail.count for detail in context['details'])
        context['total'] = total

    return render(request, 'order/user_open_order.html', context)


@login_required(login_url='/login')
def remove_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
        return redirect('/add-open-order')
    raise Http404()
