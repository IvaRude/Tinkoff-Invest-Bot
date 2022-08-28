from datetime import datetime
from typing import List

import pytz
import asyncio
import aiohttp
from tinkoff.invest import Bond, Coupon
from tinkoff.invest import Client
from tinkoff.invest.exceptions import RequestError

from config import TINKOFF_TOKEN
from tinkoff_bonds.profit_bonds import Profit_Bond

utc = pytz.UTC
LAST_DATE = utc.localize(datetime(2025, 1, 1))

BROKER_COEFF = 0.003
PROFIT_COEFF = 0.87

MAX_PERCENTAGE = 30
MIN_PERCENTAGE = 9


def get_coupon_cost(coupon: Coupon) -> float:
    return coupon.pay_one_bond.units + coupon.pay_one_bond.nano / (10 ** 9)


def count_coupon_sums_for_bonds(client: Client, bonds: List[Bond]) -> List[int]:
    n = len(bonds)
    coupon_sums = [0] * n
    for i, bond in enumerate(bonds):
        try:
            coupon_sums[i] = count_total_last_coupons_sum(client, bond)
        except RequestError as e:
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
            or bond.perpetual_flag \
            or bond.floating_coupon_flag:
        return False
    return True


def collect_bonds_info(client: Client) -> List[Profit_Bond]:
    bonds = list(filter(filter_bond, client.instruments.bonds().instruments))
    figis = [bond.figi for bond in bonds]
    prices = client.market_data.get_last_prices(figi=figis).last_prices
    prices = [(price.price.units + price.price.nano / 10 ** 9) * 10 for price in prices]
    coupon_sums = count_coupon_sums_for_bonds(client, bonds)
    profit_bonds = [None] * len(bonds)
    for i, bond in enumerate(bonds):
        profit_bond = Profit_Bond(bond)
        profit_bond.price = prices[i]
        profit_bond.coupon_sum = coupon_sums[i]
        profit_bond.count_profit_percentage()
        profit_bonds[i] = profit_bond
    return profit_bonds


def find_best_bonds_in_interval_percents(max_percentage=MAX_PERCENTAGE, min_percentage=MIN_PERCENTAGE) -> \
        List[Profit_Bond]:
    with Client(TINKOFF_TOKEN) as client:
        profit_bonds = collect_bonds_info(client)
        profit_bonds.sort(key=lambda bond: -bond.profit_percentage)
        start_ind = -1
        for i, bond in enumerate(profit_bonds):
            if bond.profit_percentage <= max_percentage:
                start_ind = i
                break
        if start_ind == -1:
            return []
        for i, bond in enumerate(profit_bonds[start_ind:]):
            if bond.profit_percentage < min_percentage:
                return profit_bonds[start_ind:start_ind + i]
        return profit_bonds[start_ind:]


def filter_bonds_by_rate(bonds: List[Profit_Bond], rate: str) -> List[Profit_Bond]:
    if rate == 'all':
        return bonds
    return [bond for bond in bonds if bond.get_rate() == rate]


async def async_filter_bonds_by_rate(bonds: List[Profit_Bond], rate: str) -> List[Profit_Bond]:
    if rate == 'all':
        return bonds
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(bond.async_get_rate(session)) for bond in bonds]
        await asyncio.gather(*tasks)
    return [bond for bond in bonds if bond.rate == rate]

def best_bonds_message(rate: str = 'all') -> str:
    try:
        bonds = find_best_bonds_in_interval_percents()
    except:
        bonds = None
    if not bonds:
        return 'Нет подходящих облигаций'
    bonds = filter_bonds_by_rate(bonds, rate)
    # bonds = await async_filter_bonds_by_rate(bonds, rate)
    message = ''
    for i, bond in enumerate(bonds):
        message += f'{i + 1}  -->  {bond.name} {bond.profit_percentage}%\n'
    return message

async def async_best_bonds_message(rate: str = 'all') -> str:
    try:
        bonds = find_best_bonds_in_interval_percents()
    except RequestError:
        return await async_best_bonds_message(rate)
    except:
        bonds = None
    if not bonds:
        return 'Нет подходящих облигаций'
    bonds = await async_filter_bonds_by_rate(bonds, rate)
    message = ''
    for i, bond in enumerate(bonds):
        message += f'{i + 1}  -->  {bond.name}:  {bond.profit_percentage}%\n'
    return message
