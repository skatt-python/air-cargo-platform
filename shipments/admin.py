# shipments/admin.py

from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_owner', 'status', 'departure_city', 'arrival_city', 'created_at')
    list_filter = ('status', 'cargo_type', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'departure_city', 'arrival_city')
    readonly_fields = ('created_at', 'updated_at', 'views', 'volume_display')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'owner', 'status', 'description')
        }),
        ('Детали груза', {
            'fields': (
            'cargo_type', 'weight', 'length', 'width', 'height', 'volume_display', 'packaging', 'is_hazardous')
        }),
        ('Маршрут', {
            'fields': ('departure_city', 'departure_country', 'arrival_city', 'arrival_country')
        }),
        ('Даты', {
            'fields': ('departure_date', 'latest_departure_date', 'arrival_date', 'latest_arrival_date')
        }),
        ('Финансы', {
            'fields': ('estimated_price', 'currency', 'payment_method', 'incoterm', 'additional_costs')
        }),
        ('Статистика', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_owner(self, obj):
        return obj.owner.username

    get_owner.short_description = 'Владелец'
    get_owner.admin_order_field = 'owner__username'

    def volume_display(self, obj):
        return f"{obj.volume:.2f} м³"

    volume_display.short_description = 'Объем'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('owner')