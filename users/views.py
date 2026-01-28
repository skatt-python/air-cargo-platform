from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Временно создадим формы здесь, чтобы избежать циклического импорта
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Временные CHOICES
USER_TYPE_CHOICES_TEMP = (
    ('customer', '👤 Грузовладелец'),
    ('agent', '👔 Агент перевозок'),
    ('developer', '👨‍💻 Разработчик'),
)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    company_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название вашей компании'
        })
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES_TEMP,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'company_name', 'user_type', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль (минимум 8 символов)'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })

        if 'username' in self.fields:
            del self.fields['username']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )


# Views функции
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            user_type_display = dict(USER_TYPE_CHOICES_TEMP).get(user.user_type, user.user_type)
            messages.success(
                request,
                f'🎉 Добро пожаловать, {user.company_name}! '
                f'Ваш аккаунт ({user_type_display}) успешно создан.'
            )

            if user.user_type == 'customer':
                return redirect('shipment_list')
            elif user.user_type == 'agent':
                return redirect('shipment_list')
            else:
                return redirect('home')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            user_type_display = dict(USER_TYPE_CHOICES_TEMP).get(user.user_type, user.user_type)
            messages.success(
                request,
                f'👋 Добро пожаловать обратно, {user.company_name}! '
                f'({user_type_display})'
            )

            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            elif user.user_type == 'customer':
                return redirect('shipment_list')
            elif user.user_type == 'agent':
                return redirect('shipment_list')
            else:
                return redirect('home')
        else:
            messages.error(request, '❌ Неверный email или пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        messages.info(request, f'👋 До свидания, {request.user.company_name}! Вы вышли из системы.')
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    # Разные данные для разных типов пользователей
    if user.user_type == 'customer':
        from shipments.models import Shipment
        user_shipments = Shipment.objects.filter(customer=user).order_by('-created_at')[:5]
        context['shipments'] = user_shipments

    elif user.user_type == 'agent':
        from bids.models import Bid
        user_bids = Bid.objects.filter(agent=user).order_by('-created_at')[:5]
        context['bids'] = user_bids

    return render(request, 'users/dashboard.html', context)