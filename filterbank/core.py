import filterbank.accumulators as accumulators
import filterbank.encoders as encoders
from filterbank.tabfile import Reader

class BlockDigester:
    def __init__(self, block_size, channel_config, output_location):
        self.seen_rows = 0
        #Accumulators bypassed if we are just doing single values
        if block_size == 1:
            channel_config['accumulators'] = ['LastVal']
        self.block_size = block_size
        self.evaluator = compile(channel_config['value'], '<string>', 'eval')
        self.accumulators = [accumulators(accum) for accum in channel_config['accumulators']]
        self.encoder = encoders(channel_config['encoder'])
        self.encoder.start(output_location, channel_config, block_size)
    def process_row(self, row):
        value = eval(self.evaluator, {}, row)
        for accum in self.accumulators:
            accum(value)
        self.seen_rows += 1
        if self.seen_rows == self.block_size:
            self.end_block()
    def end_block(self):
        self.seen_rows = 0
        for accum in self.accumulators:
            self.encoder.write(accum.result())
    def finish(self):
        if self.seen_rows > 0:
            self.end_block()
        self.encoder.finish()

def geometric_series(start, max, mult):
    result = []
    while True:
        result.append(start)
        start *= mult
        if start > max:
            break
    return result

class FilterBankProcessor:
    def __init__(self, input_file, output_location, config):
        self.block_sizes =  geometric_series(config['block_sizes']['start'], config['block_sizes']['end'], config['block_sizes'].get('mult',10))
        self.reader = Reader(input_file)
        self.output_location = output_location
        self.channel_configs = [dict({'name':name},**chan_config) for name, chan_config in config['channels'].items()]

    def process(self):
        digesters = [BlockDigester(block_size, channel_config, self.output_location)
                             for block_size in self.block_sizes
                               for channel_config in self.channel_configs]
        for entry in self.reader:
            for digester in digesters:
                digester.process_row(entry)
        for digester in digesters:
            digester.finish()





