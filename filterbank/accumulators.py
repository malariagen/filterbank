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
        return self.count/self.sum

class Median(Accumulator):
    def reset(self):
        self.elements = []
    def __call__(self, element):
        self.elements.append(element)
    def result(self):
        self.elements.sort()
        a = self.elements
        return float((a[len(a)//2] + a[-(len(a)+1)//2]))/2

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

