from django.contrib.auth import get_user_model
from requests import RequestException
from rest_framework.decorators import api_view, schema, action, \
    permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from wallets.models import Currency, Wallet
from wallets.serializers import CurrencyListSerializer, WalletSerializer, \
    AddMoneySerializer
from wallets.services.cb_rates_api import get_cb_exchange_rate
from wallets.services.wallet import add_money

User = get_user_model()


class CurrencyListView(ListModelMixin, GenericViewSet):
    """Список курсов валют"""
    queryset = Currency.objects.all().order_by('symbol')
    serializer_class = CurrencyListSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
# @schema(None)
def get_currency_exchange_rate(request, from_currency, to_currency):
    """Получить курс обмена между валютами из ЦБ"""
    context = {}
    try:
        result = get_cb_exchange_rate(from_currency, to_currency)
        context['rate'] = result
        response_status = status.HTTP_200_OK
    except ValueError:
        context['error'] = 'Данные не найдены'
        response_status = status.HTTP_400_BAD_REQUEST
    except RequestException:
        context['error'] = 'Сервис не доступен'
        response_status = status.HTTP_503_SERVICE_UNAVAILABLE

    # serializer = RateExchangeSerializer(context['rate'])
    # return Response(data=serializer.data, status=response_status)
    # todo swagger doc response
    return Response(data=context, status=response_status)


class WalletViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список пользователей системы"""
    queryset = Wallet.objects.all().select_related('user').\
        order_by('serial_number')
    serializer_class = WalletSerializer
    permission_classes = [AllowAny]
    lookup_field = 'serial_number'

    @action(detail=False, methods=['post'], name='Add money',
            serializer_class=AddMoneySerializer,
            permission_classes=[IsAuthenticated])
    def add_money(self, request):
        """Пополнение баланса"""
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        context = {}
        try:
            wallet = add_money(user=user, amount=serializer.data['amount'])
            context['result'] = {
                'serial_number': wallet.serial_number,
                'balance': wallet.balance
            }
            response_status = status.HTTP_200_OK
        except ValueError as e:
            context['error'] = f'Некорректный запрос. {e.__str__()}'
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(data=context, status=response_status)
