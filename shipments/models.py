# shipments/models.py - исправленная версия

from django.db import models
from django.conf import settings


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активна'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
        ('inactive', 'Неактивна'),
    ]

    CARGO_TYPE_CHOICES = [
        ('general', 'Генеральный груз'),
        ('perishable', 'Скоропортящийся груз'),
        ('dangerous', 'Опасный груз'),
        ('live_animals', 'Живые животные'),
        ('valuable', 'Ценный груз'),
        ('oversized', 'Крупногабаритный груз'),
        ('refrigerated', 'Рефрижераторный груз'),
    ]

    PACKAGING_CHOICES = [
        ('pallet', 'Паллет'),
        ('box', 'Коробка'),
        ('crate', 'Ящик'),
        ('bag', 'Мешок'),
        ('barrel', 'Бочка'),
        ('container', 'Контейнер'),
        ('none', 'Без упаковки'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Банковский перевод'),
        ('letter_of_credit', 'Аккредитив'),
        ('cash', 'Наличные'),
        ('escrow', 'Эскроу-счет'),
        ('other', 'Другое'),
    ]

    INCOTERM_CHOICES = [
        ('exw', 'EXW - Франко завод'),
        ('fca', 'FCA - Франко перевозчик'),
        ('cpt', 'CPT - Фрахт/перевозка оплачены до'),
        ('cip', 'CIP - Фрахт/перевозка и страхование оплачены до'),
        ('dat', 'DAT - Поставка на терминале'),
        ('dap', 'DAP - Поставка в месте назначения'),
        ('ddp', 'DDP - Поставка с оплатой пошлины'),
    ]

    # Основная информация
    title = models.CharField('Название заявки', max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name='Владелец'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    description = models.TextField('Описание', blank=True)

    # Детали груза
    cargo_type = models.CharField(
        'Тип груза',
        max_length=20,
        choices=CARGO_TYPE_CHOICES,
        default='general'
    )
    weight = models.DecimalField(
        'Вес (кг)',
        max_digits=10,
        decimal_places=2
    )
    length = models.DecimalField(
        'Длина (см)',
        max_digits=10,
        decimal_places=2
    )
    width = models.DecimalField(
        'Ширина (см)',
        max_digits=10,
        decimal_places=2
    )
    height = models.DecimalField(
        'Высота (см)',
        max_digits=10,
        decimal_places=2
    )
    packaging = models.CharField(
        'Упаковка',
        max_length=20,
        choices=PACKAGING_CHOICES,
        blank=True
    )
    is_hazardous = models.BooleanField('Опасный груз', default=False)

    # Маршрут
    departure_city = models.CharField('Город отправления', max_length=100)
    departure_country = models.CharField('Страна отправления', max_length=100)
    arrival_city = models.CharField('Город назначения', max_length=100)
    arrival_country = models.CharField('Страна назначения', max_length=100)

    # Даты
    departure_date = models.DateField('Желаемая дата отправления')
    latest_departure_date = models.DateField('Крайняя дата отправления', blank=True, null=True)
    arrival_date = models.DateField('Желаемая дата прибытия')
    latest_arrival_date = models.DateField('Крайняя дата прибытия', blank=True, null=True)

    # Финансы
    estimated_price = models.DecimalField(
        'Ожидаемая стоимость',
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(
        'Валюта',
        max_length=3,
        default='USD',
        choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')]
    )
    payment_method = models.CharField(
        'Метод оплаты',
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='bank_transfer'
    )
    incoterm = models.CharField(
        'Инкотермс',
        max_length=10,
        choices=INCOTERM_CHOICES,
        default='fca'
    )
    additional_costs = models.TextField('Дополнительные расходы', blank=True)

    # Статистика
    views = models.PositiveIntegerField('Просмотры', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    # Связь с принятым предложением
    accepted_bid = models.OneToOneField(
        'bids.Bid',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_for_shipment',
        verbose_name='Принятое предложение'
    )

    class Meta:
        verbose_name = 'Заявка на перевозку'
        verbose_name_plural = 'Заявки на перевозку'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} (#{self.id})'

    @property
    def volume(self):
        """Рассчитать объем груза в м³"""
        if all([self.length, self.width, self.height]):
            # Переводим из см³ в м³
            return (self.length * self.width * self.height) / 1000000
        return 0