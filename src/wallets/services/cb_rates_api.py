import logging

import requests
from requests import RequestException

from config.settings import HTTP_TIMEOUT


logger = logging.getLogger('wallets')
CB_URL = 'https://api.exchangeratesapi.io/latest?base='


def get_cb_currency_rates(base_currency):
    """
    Получение всех доступных курсов валют на текщий момент API
    --> {"RUB": 1.0, "EUR": 0.0109973859, .......}
    """
    url = f'{CB_URL}{base_currency}'
    try:
        response = requests.request(method='GET', url=url,
                                    timeout=HTTP_TIMEOUT)
    except RequestException as e:
        logger.error(f'Get currency rates. Service not available. {e}')
        raise e
    response_json = response.json()
    rates = response_json.get('rates')
    error = response_json.get('error')
    if error:
        logger.error(f'Error when getting currency from CB. {error}')
        raise ValueError(f"Error when getting currency from CB. {error}")
    logger.info(f'Getting all available rates with base: {base_currency}')
    return rates


def get_cb_exchange_rate(from_currency, to_currency, base_currency):
    """
    Получение курса обмена между указанными валютами
    --> {"USD": 0.013188569, "GBP": 0.0096262147}
    """

    url = '{0}{1}&symbols={2},{3}'.\
        format(CB_URL, from_currency, to_currency, base_currency)
    try:
        response = requests.request(method='GET', url=url,
                                    timeout=HTTP_TIMEOUT)
    except requests.exceptions.RequestException as e:
        logger.error(f'Get currency exchange rates. '
                     f'Service not available. {e}')
        raise e
    response_json = response.json()
    rates = response_json.get('rates')
    error = response_json.get('error')
    text = f'{from_currency} to {to_currency}, base {base_currency} {error}'
    if error:
        logger.error(f'text_error')
        raise ValueError('Error when getting rates exchange from CB. ' + text)
    logger.info('Getting currency exchange rates. ' + text)
    return rates
