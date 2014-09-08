#! /usr/bin/env python

from startup import *
from mrd.context import Context

## Test Context class

class TestContextFunctions(unittest.TestCase):

    def setUp(self):
        # Instantiate a Context object
        self.context = Context()

    def tearDown(self):
        # Release instantiated objects
        del self.context

    def test_init(self):
        self.assertIsNone(self.context.language)
        self.assertIsNone(self.context.type)

suite = unittest.TestLoader().loadTestsFromTestCase(TestContextFunctions)

## Run test suite

testResult = unittest.TextTestRunner(verbosity=2).run(suite)
