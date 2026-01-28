from django import forms
from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'currency', 'departure_date', 'arrival_date', 'notes']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'departure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'arrival_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Дополнительная информация о предложении...'
            }),
        }
        labels = {
            'price': 'Цена перевозки',
            'currency': 'Валюта',
            'departure_date': 'Дата отправления',
            'arrival_date': 'Дата прибытия',
            'notes': 'Дополнительные заметки',
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        arrival_date = cleaned_data.get('arrival_date')

        if departure_date and arrival_date:
            if departure_date > arrival_date:
                raise forms.ValidationError(
                    'Дата отправления не может быть позже даты прибытия.'
                )

        return cleaned_data