from django.urls import path

from . import views


urlpatterns = [
    path('', views.DashView.as_view(), name='dash'),
    path('engine/', views.EngineList.as_view(), name='engine_list'),
    path('engine_create/',
         views.EngineCreate.as_view(),
         name='engine_create'
         ),
    path('engine_update/<int:pk>',
         views.EngineUpdate.as_view(),
         name='engine_update'
         ),
    path('operation/', views.OperationList.as_view(), name='operation_list'),
    path('opeation_create/',
         views.OperationCreate.as_view(),
         name='operation_create'
         ),
    path('operation_update/<int:pk>',
         views.OperationUpdate.as_view(),
         name='operation_update'
         ),
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
    path('order_pdf/<int:pk>', views.order_pdf, name='order_pdf'),
]
