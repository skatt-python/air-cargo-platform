# shipments/forms.py - исправленная версия

from django import forms
from .models import Shipment


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'title', 'description', 'cargo_type', 'weight',
            'length', 'width', 'height', 'packaging', 'is_hazardous',
            'departure_city', 'departure_country', 'arrival_city', 'arrival_country',
            'departure_date', 'latest_departure_date', 'arrival_date', 'latest_arrival_date',
            'estimated_price', 'currency', 'payment_method', 'incoterm', 'additional_costs'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Перевозка оборудования из Москвы в Берлин'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишите детали груза, особые требования...'
            }),
            'cargo_type': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'length': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'см'
            }),
            'width': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'см'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'см'
            }),
            'packaging': forms.Select(attrs={'class': 'form-control'}),
            'is_hazardous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'departure_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Москва'
            }),
            'departure_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Россия'
            }),
            'arrival_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Берлин'
            }),
            'arrival_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Германия'
            }),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'latest_departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'latest_arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estimated_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'incoterm': forms.Select(attrs={'class': 'form-control'}),
            'additional_costs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Таможенные пошлины, страхование и т.д.'
            }),
        }
        labels = {
            'title': 'Название заявки',
            'description': 'Описание',
            'cargo_type': 'Тип груза',
            'weight': 'Вес (кг)',
            'length': 'Длина (см)',
            'width': 'Ширина (см)',
            'height': 'Высота (см)',
            'packaging': 'Упаковка',
            'is_hazardous': 'Опасный груз',
            'departure_city': 'Город отправления',
            'departure_country': 'Страна отправления',
            'arrival_city': 'Город назначения',
            'arrival_country': 'Страна назначения',
            'departure_date': 'Желаемая дата отправления',
            'latest_departure_date': 'Крайняя дата отправления',
            'arrival_date': 'Желаемая дата прибытия',
            'latest_arrival_date': 'Крайняя дата прибытия',
            'estimated_price': 'Ожидаемая стоимость',
            'currency': 'Валюта',
            'payment_method': 'Метод оплаты',
            'incoterm': 'Инкотермс',
            'additional_costs': 'Дополнительные расходы',
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        latest_departure_date = cleaned_data.get('latest_departure_date')
        arrival_date = cleaned_data.get('arrival_date')
        latest_arrival_date = cleaned_data.get('latest_arrival_date')

        # Проверка дат
        if departure_date and latest_departure_date:
            if departure_date > latest_departure_date:
                raise forms.ValidationError(
                    'Желаемая дата отправления не может быть позже крайней даты отправления.'
                )

        if arrival_date and latest_arrival_date:
            if arrival_date > latest_arrival_date:
                raise forms.ValidationError(
                    'Желаемая дата прибытия не может быть позже крайней даты прибытия.'
                )

        if departure_date and arrival_date:
            if departure_date > arrival_date:
                raise forms.ValidationError(
                    'Дата отправления не может быть позже даты прибытия.'
                )

        return cleaned_data