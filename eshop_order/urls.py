from django.urls import path

from .views import AddUserOrderView,user_open_order,remove_order_detail

app_name = 'order'

urlpatterns = [
    path('add-user-order/', AddUserOrderView.as_view(), name='user_order'),
    path('add-open-order/',user_open_order,name='open_order'),
    path('remove-order-detail/<detail_id>', remove_order_detail, name='delete_order'),
]

