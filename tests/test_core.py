import contextlib
import errno
from os import path
import shutil
import unittest
import tempfile
import yaml

import filterbank.core as core

class TestCore(unittest.TestCase):
    def setUp(self):
        self.my_dir = tempfile.mkdtemp()
    def tearDown(self):
        try:
            pass
            shutil.rmtree(self.my_dir)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
    @contextlib.contextmanager
    def fileAsString(self, *file):
        with open(path.join(self.my_dir, *file), 'r') as f:
            yield f.read()
    def assertFileExists(self, *file):
        self.assertTrue(path.exists(path.join(self.my_dir, *file)), str(file)+"doesn't exist")
    def assertFileContents(self, contents, *file):
        with self.fileAsString(*file) as output:
            self.assertEqual(contents, output, str(file) +'contents were wrong')
    def copyFixture(self, filename):
        shutil.copy(path.join(path.dirname(__file__), 'fixtures', filename), path.join(self.my_dir, filename))

    #TODO: Should prob use mock accum and encode
    def test_filter_bank_processor(self):
        self.copyFixture('test.tab')
        self.copyFixture('test.yaml')
        with open(path.join(self.my_dir, 'test.yaml'),'r') as file:
            config = yaml.load(file)
        p = core.FilterBankProcessor(path.join(self.my_dir, 'test.tab'), self.my_dir, config)
        p.process()
        self.assertFileExists('TestChannel_00000001.yaml')
        self.assertFileExists('TestChannel_00000004.yaml')
        self.assertFileExists('TestChannel_00000016.yaml')
        self.assertFileExists('TestChannel_00000001.data')
        self.assertFileExists('TestChannel_00000004.data')
        self.assertFileExists('TestChannel_00000016.data')
        #Check that block size 1 has been dealt with
        self.assertFileContents("""accumulators: [LastVal]
block_size: 1
encoder: TabDelimited
name: TestChannel
value: random*sine
"""
            , 'TestChannel_00000001.yaml')

