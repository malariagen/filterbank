import csv
import gzip
import codecs

def trytoFloat(string):
    try:
        return float(string)
    except ValueError:
        return string

class Reader:
    def __init__(self, file):
        if file[-2:] == 'gz':
            self.file = codecs.getreader("utf-8")(gzip.GzipFile(file, 'r'))
        else:
            self.file = open(file, 'r')
        dialect = csv.Sniffer().sniff(self.file.read(2048))
        self.file.seek(0)
        reader = csv.reader(self.file, dialect)
        #Read a line so we get the fieldnames loaded
        self.field_names = next(reader)
        self.reader = csv.reader(self.file, dialect)
    def fieldnames(self):
        return self.field_names
    def __iter__(self):
        return self
    def __next__(self):
        return dict(zip(self.field_names,map(trytoFloat,next(self.reader))))
    def __del__(self):
        self.file.close()

