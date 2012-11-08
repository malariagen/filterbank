import argparse
import yaml
import logging
from filterbank.logger import log
from filterbank.core import FilterBankProcessor

def commandLineInvocation():
    parser = argparse.ArgumentParser(description='Process files in a given directory')
    parser.add_argument('input_file', action='store', help='Tab delimited file')
    parser.add_argument('output_location', action='store', help='Output directory')
    parser.add_argument('--config', '-c', default=False, action='store', help='Config file to use', required=True)
    parser.add_argument('--verbose', '-v', default=False, action='store_true', help='Print details of processing')
    args = parser.parse_args()
    #noinspection PyBroadException
    try:
        with open(args.config,'r') as file:
            config = yaml.load(file)
    except:
        log.exception("\tError loading config from {file}".format(file=args.config))
        return
    log.set_verbosity(logging.INFO if args.verbose else logging.ERROR)
    fb = FilterBankProcessor(args.input_file, args.output_location, config)
    fb.process()
