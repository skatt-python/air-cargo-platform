from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Bid
from shipments.models import Shipment
from .forms import BidForm


@login_required
def create_bid(request, shipment_id):
    """Создание предложения к заявке"""
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Проверяем, что пользователь - агент перевозчика
    if not request.user.userprofile.is_carrier_agent:
        messages.error(request, 'Только агенты перевозчиков могут создавать предложения.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    # Проверяем, что заявка активна
    if shipment.status != 'active':
        messages.error(request, 'Нельзя создать предложение для неактивной заявки.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    # Проверяем, что это не заявка самого пользователя
    if shipment.owner == request.user:
        messages.error(request, 'Нельзя создать предложение к своей собственной заявке.')
        return redirect('shipment_detail', shipment_id=shipment_id)

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.shipment = shipment
            bid.carrier_agent = request.user

            # Проверяем, нет ли уже активного предложения от этого агента
            existing_bid = Bid.objects.filter(
                shipment=shipment,
                carrier_agent=request.user,
                status__in=['pending', 'accepted']
            ).first()

            if existing_bid:
                messages.error(request, 'У вас уже есть активное предложение для этой заявки.')
                return redirect('shipment_detail', shipment_id=shipment_id)

            bid.save()
            messages.success(request, 'Предложение успешно создано!')
            return redirect('shipment_detail', shipment_id=shipment_id)
    else:
        form = BidForm(initial={
            'price': shipment.estimated_price,
            'currency': shipment.currency,
            'departure_date': shipment.departure_date,
            'arrival_date': shipment.arrival_date,
        })

    return render(request, 'bids/create_bid.html', {
        'form': form,
        'shipment': shipment,
    })


@login_required
def bid_detail(request, bid_id):
    """Детальная страница предложения"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем права доступа
    if not (request.user == bid.carrier_agent or request.user == bid.shipment.owner):
        messages.error(request, 'У вас нет прав для просмотра этого предложения.')
        return redirect('dashboard')

    return render(request, 'bids/bid_detail.html', {
        'bid': bid,
        'can_accept': bid.can_be_accepted() and request.user == bid.shipment.owner,
        'can_reject': bid.can_be_rejected() and request.user == bid.shipment.owner,
        'can_cancel': bid.can_be_cancelled() and request.user == bid.carrier_agent,
    })


@login_required
@require_POST
def accept_bid(request, bid_id):
    """Принятие предложения"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем, что пользователь - владелец заявки
    if request.user != bid.shipment.owner:
        messages.error(request, 'Только владелец заявки может принимать предложения.')
        return redirect('dashboard')

    if bid.accept():
        messages.success(request, 'Предложение принято! Заявка переведена в статус "В работе".')
    else:
        messages.error(request, 'Не удалось принять предложение.')

    return redirect('shipment_detail', shipment_id=bid.shipment.id)


@login_required
@require_POST
def reject_bid(request, bid_id):
    """Отклонение предложения"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем, что пользователь - владелец заявки
    if request.user != bid.shipment.owner:
        messages.error(request, 'Только владелец заявки может отклонять предложения.')
        return redirect('dashboard')

    if bid.reject():
        messages.success(request, 'Предложение отклонено.')
    else:
        messages.error(request, 'Не удалось отклонить предложение.')

    return redirect('shipment_detail', shipment_id=bid.shipment.id)


@login_required
@require_POST
def cancel_bid(request, bid_id):
    """Отмена предложения агентом"""
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем, что пользователь - агент, создавший предложение
    if request.user != bid.carrier_agent:
        messages.error(request, 'Только создатель предложения может его отменить.')
        return redirect('dashboard')

    if bid.cancel():
        messages.success(request, 'Предложение отменено.')
    else:
        messages.error(request, 'Не удалось отменить предложение.')

    return redirect('shipment_detail', shipment_id=bid.shipment.id)