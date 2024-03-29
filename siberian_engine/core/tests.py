from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import DashView, EngineList, OperationList, OrderList


class CoreViewTest(TestCase):
    def test_dash_view(self):
        response = self.client.get(reverse('dash'))
        self.assertEqual(response.status_code, 200)

    def test_engine_list_view(self):
        response = self.client.get(reverse('engine_list'))
        self.assertEqual(response.status_code, 200)

    def test_operation_list_view(self):
        response = self.client.get(reverse('operation_list'))
        self.assertEqual(response.status_code, 200)

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)


class CoreUrlTest(SimpleTestCase):

    def test_dash_url(self):
        url = reverse('dash')
        self.assertEqual(resolve(url).func.view_class, DashView)

    def test_engine_url(self):
        url = reverse('engine_list')
        self.assertEqual(resolve(url).func.view_class, EngineList)

    def test_operation_url(self):
        url = reverse('operation_list')
        self.assertEqual(resolve(url).func.view_class, OperationList)

    def test_order_url(self):
        url = reverse('order_list')
        self.assertEqual(resolve(url).func.view_class, OrderList)
