import logging
import marketValues

class Strategy1:
    def __init__(self, currencyPair, limit):
        self.log = logging.getLogger('Strategy1')
        self.currencyPair = currencyPair
        self.limit = limit
        self.mv = marketValues.marketValues()
        self.pavg = None
        self.ppavg = None
        self.pema = None
        self.ppema = None
        self.extema = None
        self.pextema = None
        self.position = None
        self.stopLimit = None
        self.cost = None
        self.totalProfit = float(0);
        self.i = 0

    def poll(self, ticker):
        interval1 = 240
        interval2 = 1440
        limitFactor = 1.33
        t = ticker[self.currencyPair]
        v = float(t['last'])
        self.mv.next(v)
        self.ppavg = self.pavg
        self.pavg = self.mv.getSma(interval1)
        self.ppema = self.pema
        self.pema = self.mv.getEma(interval1)
        stddev = self.mv.getMovStddev(interval1)
        extsma = self.mv.getSma(interval2)
        self.pextema = self.extema
        self.extema = self.mv.getEma(interval2)
        # extema = self.mv.getEma(interval2)
        self.log.debug('{}| v: {}, sma: {}, ema: {}, stddev: {}'.format(self.currencyPair, v, self.pavg, self.pema, stddev))
        if self.pavg != None and self.ppavg != None and self.pema != None and self.ppema != None and stddev != None:
            if self.position == None:
                # if self.pema > self.ppema and self.pavg < self.pema and v < (self.pavg - stddev * 0.25):
                if self.pema > self.ppema and v < extsma and self.pema < extsma:
                    self.position = self.limit / v
                    self.cost = self.position * v
                    stddev = self.mv.getMovStddev(interval1)
                    if stddev != None:
                        self.stopLimit = v - (limitFactor * stddev)
                        #self.stopLimit = self.findStopLimit(self.currencyPair)
                        self.log.warning('{}| BUY({}) cost: {}, stopLimit: {}'.format(self.currencyPair, self.position, self.cost, self.stopLimit))
                        #self.p.buy(self.currencyPair, v, self.position)
                        self.position *= 0.9975
            else:
                if v > self.pavg and self.i % 2 == 0:
                    if stddev != None:
                        newLimit = v - (limitFactor * stddev)
                        #newLimit = self.findStopLimit(key)
                        if newLimit > self.stopLimit:
                            self.stopLimit = newLimit
                            self.log.info('{}| cost: {}, stopLimit: {} (atPosition: {})'.format(self.currencyPair, self.cost, self.stopLimit, self.position * self.stopLimit))
                if v <= self.stopLimit:
                    sellAt = v * 0.995;
                    delta = self.position * sellAt - self.cost;
                    self.totalProfit += delta;
                    self.log.warning('{}| SELL({}, {}) take: {}, delta: {}, total-profit: {}'.format(self.currencyPair, sellAt, self.position, self.position * sellAt, delta, self.totalProfit))
                    #self.p.sell(self.currencyPair, sellAt, self.position)
                    self.position = None
                    self.stopLimit = None
                # elif v > (self.pavg + stddev * 0.33):
                #     sellAt = v * 0.995;
                #     delta = self.position * sellAt - self.cost;
                #     self.totalProfit += delta;
                #     self.log.warning('{}| SELL({}, {}) take: {}, delta: {}, total-profit: {}'.format(self.currencyPair, sellAt, self.position, self.position * sellAt, delta, self.totalProfit))
                #     #self.p.sell(self.currencyPair, sellAt, self.position)
                #     self.position = None
                #     self.stopLimit = None

        ++self.i
