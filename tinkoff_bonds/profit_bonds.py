from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tinkoff.invest import Bond
from tinkoff.invest.exceptions import RequestError

BROKER_COEFF = 0.003
PROFIT_COEFF = 0.87
URL = 'https://www.tinkoff.ru/invest/bonds/'


class Profit_Bond(Bond):
    rates = {
        'Низкий': 'low',
        'Средний': 'middle',
        'Высокий': 'high',
    }

    def __init__(self, bond: Bond):
        self.figi = bond.figi
        self.isin = bond.isin
        self.ticker = bond.ticker
        self.name = bond.name
        self.maturity_date = bond.maturity_date
        self.nominal = bond.nominal
        self.aci_value = bond.aci_value
        self.price: float = 0
        self.coupon_sum: float = 0
        self.profit_percentage: float = 0
        self.rate = 0

    def count_profit_percentage(self):
        nominal = self.nominal.units + self.nominal.nano / 10 ** 9
        profit = nominal + self.coupon_sum * PROFIT_COEFF
        expenses = (self.price + self.aci_value.units + self.aci_value.nano / 10 ** 9) * (1 + BROKER_COEFF)
        start_date = datetime.now()
        num_of_months = (self.maturity_date.year - start_date.year) * 12 + (self.maturity_date.month - start_date.month)
        if num_of_months:
            self.profit_percentage = round((profit / expenses - 1) / num_of_months * 12 * 100, 2)
        else:
            self.profit_percentage = round((profit / expenses - 1) * 12 * 100, 2)

    def get_rate(self) -> str:
        headers = {
            'User-Agent': 'Chrome 1.0',
        }
        response = requests.get(URL + self.ticker + '/', headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            rate_word = soup.find_all('div', class_='SecurityHeader__panelText_KDJdO')[-1].text
            return self.rates.get(rate_word, 'NULL')
        except RequestError:
            pass
        except:
            return 'NULL'
