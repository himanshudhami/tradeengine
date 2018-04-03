import math

class marketValues:
    def __init__(self, values = []):
        self.values = values

    def next(self, value):
        self.values.insert(0, float(value))

    def getSma(self, count, skip = 0):
        if count + skip > len(self.values):
            return None
        return sum(self.values[skip:skip+count]) / count;

    # def getSmaSlope(self, count, skip = 0):
    #     if count + skip > len(self.values):
    #         return None
    #     return self.getSma(count, skip) - self.getSma(count, skip + 1)

    def getEma(self, count):
        if count > len(self.values):
            return None
        value = self.getSma(count)
        k = float(2) / float(count + 1)
        for i in range(count - 1, -1, -1):
            value = (self.values[i] - value) * k + value
        return value

    def getStddev(self, count, skip = 0):
        try:
            avg = self.getSma(count, skip);
            value = 0
            for i in range(skip, skip+count):
                value += pow(self.values[i] - avg, 2)
            value = math.sqrt(value / (count - 1))
            return value
        except:
            return None

    def getMovStddev(self, count):
        try:
            values = []
            for i in range(0, count):
                values.append(self.values[i] - self.getSma(count, i))
            return marketValues(values).getStddev(count);
        except:
            return None
