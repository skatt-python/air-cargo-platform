from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipment_list, name='shipment_list'),
    path('create/', views.shipment_create, name='shipment_create'),
    path('<int:shipment_id>/', views.shipment_detail, name='shipment_detail'),
    path('<int:shipment_id>/edit/', views.shipment_edit, name='shipment_edit'),
    path('<int:shipment_id>/delete/', views.shipment_delete, name='shipment_delete'),
    path('<int:shipment_id>/deactivate/', views.shipment_deactivate, name='shipment_deactivate'),
]