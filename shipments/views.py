from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST  # Добавьте эту строку

from .models import Shipment
from .forms import ShipmentForm
from bids.models import Bid
from bids.forms import BidForm


def shipment_list(request):
    """Список всех заявок с фильтрацией"""
    shipments = Shipment.objects.all().order_by('-created_at')

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        shipments = shipments.filter(status=status_filter)

    # Фильтрация по типу груза
    cargo_type = request.GET.get('cargo_type')
    if cargo_type:
        shipments = shipments.filter(cargo_type=cargo_type)

    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        shipments = shipments.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(departure_city__icontains=search_query) |
            Q(arrival_city__icontains=search_query)
        )

    # Показывать только активные заявки для неавторизованных пользователей
    if not request.user.is_authenticated:
        shipments = shipments.filter(status='active')

    # Пагинация
    paginator = Paginator(shipments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shipments/shipment_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'cargo_type': cargo_type,
        'search_query': search_query,
    })


@login_required
def shipment_detail(request, shipment_id):
    """Детальная страница заявки с предложениями"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Получаем все предложения для этой заявки
    bids = shipment.bids.all()

    # Проверяем, может ли текущий пользователь создать предложение
    can_create_bid = (
            request.user.is_authenticated and
            request.user.userprofile.is_carrier_agent and
            shipment.status == 'active' and
            shipment.owner != request.user and
            not Bid.objects.filter(
                shipment=shipment,
                carrier_agent=request.user,
                status__in=['pending', 'accepted']
            ).exists()
    )

    # Форма для создания предложения (если можно)
    bid_form = None
    if can_create_bid:
        bid_form = BidForm(initial={
            'price': shipment.estimated_price,
            'currency': shipment.currency,
            'departure_date': shipment.departure_date,
            'arrival_date': shipment.arrival_date,
        })

    context = {
        'shipment': shipment,
        'bids': bids,
        'can_create_bid': can_create_bid,
        'bid_form': bid_form,
        'is_owner': request.user == shipment.owner,
    }

    return render(request, 'shipments/shipment_detail.html', context)


@login_required
def shipment_create(request):
    """Создание новой заявки"""
    if not request.user.userprofile.is_cargo_owner:
        messages.error(request, 'Только грузовладельцы могут создавать заявки.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ShipmentForm(request.POST, request.FILES)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.owner = request.user
            shipment.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('shipment_detail', shipment_id=shipment.id)
    else:
        form = ShipmentForm()

    return render(request, 'shipments/shipment_form.html', {
        'form': form,
        'title': 'Создание новой заявки'
    })


@login_required
def shipment_edit(request, shipment_id):
    """Редактирование заявки"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Проверяем права доступа
    if request.user != shipment.owner:
        messages.error(request, 'Вы не можете редактировать чужие заявки.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    # Нельзя редактировать заявку, если есть принятые предложения
    if shipment.status not in ['draft', 'active']:
        messages.error(request, 'Нельзя редактировать заявку в текущем статусе.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    if request.method == 'POST':
        form = ShipmentForm(request.POST, request.FILES, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка успешно обновлена!')
            return redirect('shipment_detail', shipment_id=shipment.id)
    else:
        form = ShipmentForm(instance=shipment)

    return render(request, 'shipments/shipment_form.html', {
        'form': form,
        'title': 'Редактирование заявки',
        'shipment': shipment,
    })


@login_required
def shipment_delete(request, shipment_id):
    """Удаление заявки"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Проверяем права доступа
    if request.user != shipment.owner:
        messages.error(request, 'Вы не можете удалять чужие заявки.')
        return redirect('dashboard')

    # Проверяем статус заявки
    if shipment.status not in ['draft', 'active']:
        messages.error(request, 'Нельзя удалить заявку в текущем статусе.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    if request.method == 'POST':
        shipment.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('dashboard')

    return render(request, 'shipments/shipment_confirm_delete.html', {
        'shipment': shipment,
    })


@login_required
@require_POST  # Теперь этот декоратор будет работать
def shipment_deactivate(request, shipment_id):
    """Деактивация заявки"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Проверяем права доступа
    if request.user != shipment.owner:
        messages.error(request, 'Вы не можете деактивировать чужие заявки.')
        return redirect('dashboard')

    # Проверяем статус заявки
    if shipment.status != 'active':
        messages.error(request, 'Заявка уже не активна.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    shipment.status = 'inactive'
    shipment.save()

    messages.success(request, 'Заявка успешно деактивирована. Новые предложения не будут приниматься.')
    return redirect('shipment_detail', shipment_id=shipment_id)