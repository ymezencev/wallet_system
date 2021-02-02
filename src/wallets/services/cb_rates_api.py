import requests
from requests import RequestException

from config.settings import HTTP_TIMEOUT


def get_cb_currency_rates(base_currency):
    """
    Получение всех доступных курсов валют на текщий момент API
    --> {"RUB": 1.0, "EUR": 0.0109973859, .......}
    """
    url = f'https://api.exchangeratesapi.io/latest?base={base_currency}'
    try:
        response = requests.request(method='GET', url=url,
                                    timeout=HTTP_TIMEOUT)
    except RequestException as e:
        # logging
        raise e
    response_json = response.json()
    rates = response_json.get('rates')
    error = response_json.get('error')
    if error:
        # logging
        raise ValueError(f"Error when getting currency from CB. {error}")
    # logging info
    return rates


def get_cb_exchange_rate(from_currency, to_currency, base_currency):
    """
    Получение курса обмена между указанными валютами
    --> {"USD": 0.013188569, "GBP": 0.0096262147}
    """

    url = 'https://api.exchangeratesapi.io/latest?base={0}&symbols={1},{2}'.\
        format(from_currency, to_currency, base_currency)
    try:
        response = requests.request(method='GET', url=url,
                                    timeout=HTTP_TIMEOUT)
    except requests.exceptions.RequestException as e:
        # logging
        raise e
    response_json = response.json()
    rates = response_json.get('rates')
    error = response_json.get('error')
    if error:
        # logging
        raise ValueError(
            f"Error when getting rates exchange from CB."
            f"{from_currency} to {to_currency} with base {base_currency} "
            f"{error}")
    # logging info
    return rates
