from datetime import datetime
from typing import List, Tuple

import pytz
from tinkoff.invest import Bond, Coupon
from tinkoff.invest import Client
from tinkoff.invest.exceptions import RequestError
import requests
from bs4 import BeautifulSoup
BROKER_COEFF = 0.003
PROFIT_COEFF = 0.87
URL = 'https://www.tinkoff.ru/invest/bonds/'

class Profit_Bond(Bond):
    def __init__(self):
        pass
    # def __init__(self, bond: Bond):
    #     self.figi = bond.figi
    #     self.name = bond.name
    #     self.maturity_date = bond.maturity_date
    #     self.nominal = bond.nominal
    #     self.aci_value = bond.aci_value
    #     self.price: float = 0
    #     self.coupon_sum: float = 0
    #     self.profit_percentage: float = 0
    #     self.rate = 0

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

    def set_rate(self):
        headers = {
            'User-Agent': 'Chrome 1.0',
        }
        # response = requests.get(URL + self.figi + '/', headers=headers)
        response = requests.get('https://www.tinkoff.ru/invest/bonds/RU000A100VY0/', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rate_word = soup.find('div', class_='SecurityHeader__panelText_KDJdO').prettify()
        print(rate_word)


if __name__ == '__main__':
    Profit_Bond().set_rate()
