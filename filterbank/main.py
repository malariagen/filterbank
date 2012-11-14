import argparse
import yaml
import logging
from filterbank.logger import log
from filterbank.core import FilterBankProcessor
import os.path

def parse_metadata(metadata):
    result = {}
    if metadata:
        for entry in metadata:
            if entry.count(':') != 1:
                log.error('Metadata not in "key:value" format - ignoring')
            else:
                key, val = entry.split(':')
                result[key] = val
    return result

class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)
    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)
Loader.add_constructor('!include', Loader.include)

def commandLineInvocation():
    parser = argparse.ArgumentParser(description='Process files in a given directory')
    parser.add_argument('input_file', action='store', help='Tab delimited file')
    parser.add_argument('output_location', action='store', help='Output directory')
    parser.add_argument('--config', '-c', default=False, action='store', help='Config file to use', required=True)
    parser.add_argument('--metadata', '-m', default=[], action='append', help='metadata in "key:value" form')
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help='Print details of processing')

    args = parser.parse_args()
    metadata = parse_metadata(args.metadata)
    #noinspection PyBroadException
    try:
        with open(args.config,'r') as file:
            config = yaml.load(file, Loader)
    except:
        log.exception("\tError loading config from {file}".format(file=args.config))
        return
    log.set_verbosity(logging.INFO if args.verbose else logging.ERROR)

    fb = FilterBankProcessor(args.input_file, args.output_location, config, extra_metadata=metadata)
    fb.process()
