from django.db import models
from django.conf import settings
from shipments.models import Shipment


class Bid(models.Model):
    BID_STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('expired', 'Истекло'),
        ('cancelled', 'Отменено'),
    ]

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Заявка на перевозку'
    )
    carrier_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_bids',
        verbose_name='Агент перевозчика'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена предложения'
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')],
        verbose_name='Валюта'
    )
    departure_date = models.DateField(
        verbose_name='Предлагаемая дата отправления'
    )
    arrival_date = models.DateField(
        verbose_name='Предлагаемая дата прибытия'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Дополнительные заметки'
    )
    status = models.CharField(
        max_length=20,
        choices=BID_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус предложения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['shipment', 'carrier_agent'],
                condition=models.Q(status__in=['pending', 'accepted']),
                name='unique_active_bid_per_carrier'
            )
        ]

    def __str__(self):
        return f'Предложение #{self.id} для заявки #{self.shipment.id}'

    def can_be_accepted(self):
        """Может ли предложение быть принято"""
        return self.status == 'pending' and self.shipment.status == 'active'

    def can_be_rejected(self):
        """Может ли предложение быть отклонено"""
        return self.status == 'pending'

    def can_be_cancelled(self):
        """Может ли предложение быть отменено агентом"""
        return self.status == 'pending'

    def accept(self):
        """Принять предложение"""
        if not self.can_be_accepted():
            return False

        # Отклоняем все остальные предложения для этой заявки
        Bid.objects.filter(
            shipment=self.shipment,
            status='pending'
        ).exclude(id=self.id).update(status='rejected')

        # Принимаем текущее предложение
        self.status = 'accepted'
        self.save()

        # Обновляем статус заявки
        self.shipment.status = 'in_progress'
        self.shipment.accepted_bid = self
        self.shipment.save()

        return True

    def reject(self):
        """Отклонить предложение"""
        if not self.can_be_rejected():
            return False

        self.status = 'rejected'
        self.save()
        return True

    def cancel(self):
        """Отменить предложение"""
        if not self.can_be_cancelled():
            return False

        self.status = 'cancelled'
        self.save()
        return True