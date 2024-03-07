from django.urls import path

from . import views


urlpatterns = [
     path('', views.DashView.as_view(), name='dash'),
     path('engine/', views.EngineList.as_view(), name='engine_list'),
     path('operation/', views.OperationList.as_view(), name='operation_list'),
     path('order/', views.OrderList.as_view(), name='order_list'),
     path('order_create/', views.OrderCreate.as_view(), name='order_create'),
     path('order_update/<int:pk>',
          views.OrderUpdate.as_view(),
          name='order_update'
          ),
     path('get_operations_by_engine/',
          views.get_operations_by_engine,
          name='update_operations'
          ),
]
