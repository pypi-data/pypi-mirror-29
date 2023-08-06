# -*- coding: utf-8 -*-

from __future__ import print_function
from ct_manager.api import (get_equity_market,
                            construct_portfolio_by_weight,
                            evaluate_portfolio_between_rebalance_by_weight)


# print(get_equity_market('ashare', start_date='20170101', end_date='20170201', fields=['close', 'adj_factor']))


ptf = construct_portfolio_by_weight(['000001', '000005'], ref_date='20180105', weight=[0.5, 0.5])
ret = evaluate_portfolio_between_rebalance_by_weight(ptf, '20180106', '20180109')
print(ret)