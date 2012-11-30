import filterbank.accumulators as accumulators
import filterbank.encoders as encoders
from filterbank.tabfile import Reader
import copy

class BlockDigester:
    def __init__(self, block_size, channel_config, output_location):
        self.seen_rows = 0
        #Accumulators bypassed if we are just doing single values
        if block_size == 1:
            channel_config = copy.deepcopy(channel_config)
            channel_config['accumulators'] = ['LastVal']
        self.block_size = block_size
        self.accumulators = [accumulators(accum) for accum in channel_config['accumulators']]
        self.encoder = encoders(channel_config['encoder'])
        self.encoder.start(output_location, channel_config, block_size)
    def process_value(self, value):
        for accum in self.accumulators:
            accum(value)
        self.seen_rows += 1
        if self.seen_rows == self.block_size:
            self.end_block()
    def end_block(self):
        self.seen_rows = 0
        self.encoder.write([accum.result() for accum in self.accumulators])
        for accum in self.accumulators:
            accum.reset()
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
    def __init__(self, input_file, output_location, config, extra_metadata={}):
        self.block_sizes =  geometric_series(config['block_sizes']['start'], config['block_sizes']['end'], config['block_sizes'].get('mult',10))
        self.reader = Reader(input_file)
        self.output_location = output_location
        self.channel_configs = [dict({'name':name}, **dict(extra_metadata, **chan_config)) for name, chan_config in config['channels'].items()]

    def process(self):
        evaluators_and_digesters = []
        for channel_config in self.channel_configs:
            evaluator = compile(channel_config['value'], '<string>', 'eval')
            digesters = [BlockDigester(block_size, channel_config, self.output_location) for block_size in self.block_sizes]
            evaluators_and_digesters.append((evaluator, digesters))
        for row in self.reader:
            for evaluator, digesters in evaluators_and_digesters:
                value = eval(evaluator, {}, row)
                for digester in digesters:
                    digester.process_value(value)
        for evaluator, digesters in evaluators_and_digesters:
            for digester in digesters:
                digester.finish()





