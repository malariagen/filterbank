import logging

log = logging.getLogger("filterbank")
ch = logging.StreamHandler()
#formatter = logging.Formatter('%(levelname)s - %(message)s')
#ch.setFormatter(formatter)
log.addHandler(ch)
def set_verbosity(verbosity):
    ch.setLevel(verbosity)
log.set_verbosity = set_verbosity