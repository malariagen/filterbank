import sys
import math
from filterbank.logger import log

class Accumulator:
    def __init__(self, **attrs):
        #Add in arbitary args in case any method has config
        self.__dict__.update(**attrs)
        self.reset()
    def name(self):
        return self.__class__.__name__

class LastVal(Accumulator):
    def reset(self):
        self.val = None
    def __call__(self, element):
        self.val = element
    def result(self):
        return self.val

class GeometricMean(Accumulator):
    def reset(self):
        self.sum = 0
        self.sum = 0
        self.count = 0
    def __call__(self, element):
        self.sum += 1
        self.count += element
    def result(self):
        if self.count > 0:
            return self.count/self.sum
        else:
            return None

class Median(Accumulator):
    def reset(self):
        self.elements = []
    def __call__(self, element):
        self.elements.append(element)
    def result(self):
        self.elements.sort()
        l = self.elements
        if l:
            return float((l[len(l)//2] + l[-(len(l)+1)//2]))/2
        else:
            return None

class Percentile(Accumulator):
    def reset(self):
        #Expects kwarg 'percent'
        assert(type(self.percent) == float)
        self.elements = []
    def __call__(self, element):
        self.elements.append(element)
    def result(self):
        self.elements.sort()
        l = self.elements
        if not l:
            return None
        k = (len(l)-1) * self.percent
        print(k)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return l[int(k)]
        d0 = l[int(f)] * (c-k)
        d1 = l[int(c)] * (k-f)
        return d0+d1

class Min(Accumulator):
    def reset(self):
        self.min = float("inf")
    def __call__(self, element):
        self.min = min(self.min, element)
    def result(self):
        return self.min

class Max(Accumulator):
    def reset(self):
        self.max = float("-inf")
    def __call__(self, element):
        self.max = max(self.max, element)
    def result(self):
        return self.max

#Some magic to allow us to ask the module for classes by string and dict
class Wrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __getattr__(self,name):
        return getattr(self.wrapped, name)
    def __call__(self, config):
        if type(config) == str:
            cls, kwargs = config, {}
        elif type(config) == dict:
            cls, kwargs = list(config.items())[0]
        else:
            log.error("Config for "+__name__+" is not str or dict but"+str(config))
        return getattr(self.wrapped, cls)(**kwargs)

sys.modules[__name__] = Wrapper(sys.modules[__name__])

