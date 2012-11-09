import json
import string
from os import path
import yaml
import sys

class Base64:
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+-'
    #establish the inversion table:
    invencode=[]
    for i in range(0,255):
        invencode.append(0)
    for i in range(len(alphabet)):
        invencode[ord(alphabet[i])]=i

    @staticmethod
    def encode_int(val, maxcnt=-1):
        if val is None:
            return '~'*maxcnt
        rs=''
        cnt=0
        while (val>0) or (cnt==0) or (maxcnt>0 and cnt<maxcnt):
            rs=Base64.alphabet[val & 63]+rs
            val >>= 6
            cnt+=1
        return rs

    @staticmethod
    def decode_int(st):
        rs=0
        for ch in st:
            rs=rs*64+Base64.invencode[ord(ch)]
        return rs

class Encoder:
    def __init__(self, *args, **kwattrs):
        #Add in arbitary args in case any method has config
        self.__dict__.update(**kwattrs)
    def start(self, output_location, metadata, block_size):
        filename = path.join(output_location, metadata.get('short_name',metadata['name'])+'_'+'{0:08d}'.format(block_size))
        metadata['block_size'] = block_size
        with open(filename+'.yaml', 'w') as file:
            yaml.dump(metadata, file)
        self.datafile = open(filename+'.data', 'w')
    def finish(self):
        self.datafile.close()

#Arguments: range, length=3
class FixedLengthB64(Encoder):
    def __init__(self, *args, **kwattrs):
        super().__init__(self, *args, **kwattrs)
        self.dynamic_range = int(64**self.length-10)
        self.max, self.min = self.range
        self.scaling_factor = 1.0/(self.max-self.min)*self.dynamic_range
    def write(self, value):
        if value is None:
            return '~' * self.length
        scaled_value = int(round((value-self.min)*self.scaling_factor))
        if scaled_value < 0:
            scaled_value = 0
        if scaled_value > self.dynamic_range:
            scaled_value = self.dynamic_range
        self.datafile.write(Base64.encode_int(scaled_value, self.length))


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

