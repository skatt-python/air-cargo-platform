# bids/admin.py

from django.contrib import admin
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrier_agent_info', 'shipment_info', 'price_display', 'status_display', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('shipment__title', 'carrier_agent__username', 'carrier_agent__email', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('shipment', 'carrier_agent', 'status')
        }),
        ('Детали предложения', {
            'fields': ('price', 'currency', 'departure_date', 'arrival_date', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def carrier_agent_info(self, obj):
        return f"{obj.carrier_agent.username} ({obj.carrier_agent.email})"

    carrier_agent_info.short_description = 'Агент'

    def shipment_info(self, obj):
        return f"#{obj.shipment.id}: {obj.shipment.title[:30]}..."

    shipment_info.short_description = 'Заявка'

    def price_display(self, obj):
        return f"{obj.price} {obj.currency}"

    price_display.short_description = 'Цена'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = 'Статус'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('shipment', 'carrier_agent')