from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wallets import views

router = SimpleRouter()
router.register(r'currency', views.CurrencyListView, basename='currency')
router.register(r'wallets', views.WalletViewSet, basename='wallets')

urlpatterns = [
    path('currency/exchange/<str:from_currency>/<str:to_currency>',
         views.get_currency_exchange_rate, name='currency-exchange'),
]

urlpatterns += router.urls
