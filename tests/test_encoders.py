import contextlib
import errno
from os import path
import shutil
import unittest
import tempfile

import filterbank.encoders as encoders

class TestEncoders(unittest.TestCase):
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

    def test_dynamic_load(self):
        e = encoders('TabDelimited')
        self.assertEqual(type(e), encoders.TabDelimited)
        e = encoders({'TabDelimited':{'test':'foobar'}})
        self.assertEqual(e.test, 'foobar')

class TestTabDelimited(TestEncoders):
    def testTabDelimited(self):
        e = encoders('TabDelimited')
        e.start(self.my_dir, {'name':'quango', 'accumulators':['Bob', 'Bill']}, 42)
        e.write([1,2,3])
        e.write([4,5,None])
        e.finish()
        self.assertFileExists('quango_00000042.data')
        self.assertFileContents(
        """Bob	Bill
1	2	3
4	5	None
""",
            'quango_00000042.data')
        self.assertFileExists('quango_00000042.yaml')
        self.assertFileContents(
        """accumulators: [Bob, Bill]
block_size: 42
name: quango
""",
        'quango_00000042.yaml')

class FixedLengthB64(TestEncoders):
    def testFixedLengthB64(self):
        e = encoders({'FixedLengthB64':{'length':3, 'range':[0,100]}})
        e.start(self.my_dir, {'name':'quango', 'accumulators':['Bob', 'Bill']}, 42)
        e.write([1,2,3])
        e.write([4,5,float('nan')])
        e.write([-20,500,None, float('Inf'), float('-Inf')])
        e.finish()
        self.assertFileExists('quango_00000042.data')
        self.assertFileContents(
            "Ao9BR7B64Cj1DMz~~~AAA--2~~~~~~~~~",
            'quango_00000042.data')
        self.assertFileExists('quango_00000042.yaml')
        self.assertFileContents(
            """accumulators: [Bob, Bill]
block_size: 42
name: quango
""",
            'quango_00000042.yaml')










