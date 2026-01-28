# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='shipment_list'), name='home'),

    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),  # Закомментируйте эту строку

    # Заявки
    path('shipments/', include('shipments.urls')),

    # Предложения
    path('bids/', include('bids.urls')),

    # Dashboard
    # path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)