from django.urls import path


from . import views


urlpatterns = [
    path('', views.DashView.as_view(), name='dash'),
    path('engine/', views.EngineList.as_view(), name='engine_list'),
    path('operation/', views.OperationList.as_view(), name='operation_list'),
    path('order/', views.OrderList.as_view(), name='order_list'),
    path('order/<int:pk>', views.OrderDetail.as_view(), name='order_detail'),
]
