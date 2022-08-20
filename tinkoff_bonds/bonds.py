import time
from datetime import datetime
from typing import List, Tuple

import pytz
from tinkoff.invest import Bond, Coupon
from tinkoff.invest import Client
from tinkoff.invest.exceptions import RequestError

from secrets import TINKOFF_TOKEN

utc = pytz.UTC
LAST_DATE = utc.localize(datetime(2025, 1, 1))

CHUNK_LIMIT = 199

BROKER_COEFF = 0.003
PROFIT_COEFF = 0.87


def get_coupon_cost(coupon: Coupon) -> float:
    return coupon.pay_one_bond.units + coupon.pay_one_bond.nano / (10 ** 9)


def count_coupon_sums_for_bonds(client: Client, bonds: List[Bond]) -> List[int]:
    n = len(bonds)
    ind = 0
    coupon_sums = [0] * n
    cur = n
    # while cur > CHUNK_LIMIT:
    #     for _ in range(CHUNK_LIMIT):
    #         coupon_sums[ind] = count_total_last_coupons_sum(client, bonds[ind])
    #         ind += 1
    #     cur -= CHUNK_LIMIT
    #     print(ind)
    #     time.sleep(3)
    for i in range(ind, n):
        try:
            coupon_sums[i] = count_total_last_coupons_sum(client, bonds[i])
        except RequestError as e:
            # ratelimit_reset = e.details.
            # print(e.metadata)
            pass
    return coupon_sums


def count_total_last_coupons_sum(client: Client, bond: Bond) -> int:
    bond_figi = bond.figi
    bond_last_date = bond.maturity_date
    coupons = client.instruments.get_bond_coupons(figi=bond_figi, from_=datetime.now(), to=bond_last_date).events
    ans = 0
    for coupon in coupons:
        ans += get_coupon_cost(coupon)
    return ans


def filter_bond(bond: Bond) -> bool:
    if bond.currency != 'rub' \
            or bond.maturity_date > LAST_DATE \
            or bond.maturity_date <= utc.localize(datetime.now()) \
            or bond.nominal.units != 1000 \
            or bond.perpetual_flag:
        return False
    return True


def collect_bonds_info(client: Client) -> List[Bond]:
    # bonds = list(filter(filter_bond, client.instruments.bonds().instruments))[:199]
    bonds = list(filter(filter_bond, client.instruments.bonds().instruments))
    figis = [bond.figi for bond in bonds]
    prices = client.market_data.get_last_prices(figi=figis).last_prices
    prices = [(price.price.units + price.price.nano / 10 ** 9) * 10 for price in prices]
    coupon_sums = count_coupon_sums_for_bonds(client, bonds)
    for i in range(len(bonds)):
        bonds[i].price = prices[i]
        bonds[i].coupon_sum = coupon_sums[i]
    return bonds


def count_year_percentage_for_bond(bond: Bond) -> float:
    nominal = bond.nominal.units + bond.nominal.nano / 10 ** 9
    profit = nominal + bond.coupon_sum * PROFIT_COEFF
    expenses = (bond.price + bond.aci_value.units + bond.aci_value.nano / 10 ** 9) * (1 + BROKER_COEFF)
    start_date = datetime.now()
    num_of_months = (bond.maturity_date.year - start_date.year) * 12 + (bond.maturity_date.month - start_date.month)
    if num_of_months:
        return (profit / expenses - 1) / num_of_months * 12 * 100
    return (profit / expenses - 1) * 12 * 100


def find_best_bonds() -> List[Tuple[Bond, float]]:
    with Client(TINKOFF_TOKEN) as client:
        bonds = collect_bonds_info(client)
        percentages = [count_year_percentage_for_bond(bond) for bond in bonds]
        bonds = list(zip(bonds, percentages))
        bonds.sort(key=lambda x: -x[1])
        for i, bond in enumerate(bonds):
            print(i + 1, ' --> ', bond[0].name, ' ', bond[1], '%')
        for i, bond in enumerate(bonds):
            if bond[1] <= 30:
                return bonds[i:i + 20]
        return bonds[:20]
