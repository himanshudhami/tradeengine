#!/usr/bin/env python

import logging
import dbDriver
import strategy1
import strategy2

logging.basicConfig(
    level = logging.INFO,
    #filename='tep.log',
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
log = logging.getLogger('rundb')

driver = dbDriver.DbDriver('blink', 'tep-poloniex')
strategy = strategy1.Strategy1('BTC_XMR', 100)
# strategy = strategy2.Strategy2()
driver.go(strategy)
