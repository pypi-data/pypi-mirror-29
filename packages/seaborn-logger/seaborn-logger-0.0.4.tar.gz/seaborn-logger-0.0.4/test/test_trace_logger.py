__author__ = 'Ben Christenson'
__date__ = "1/5/18"

import unittest
from seaborn.logger.logger import *

class traceTest(unittest.TestCase):
    def test_basic(self):
        log_file = os.path.join(os.path.split(__file__)[0],
                                __file__[:-3].replace('.','')+'.log')
        format = SeabornFormatter(relative_pathname= "/seaborn/seaborn/")
        format.setup_logging(log_filename=log_file,
                             log_level='TRACE',
                             log_stdout_level='TRACE')
        msg = 'testing'
        log.trace(msg)
        hello()
        return log

    def test_rotating_import(self):
        log = self.test_basic()
        try:
            import A
            import B_2
        except BaseException as e:
            log.trace(e.message)

def hello():
    log.trace('Hello!')

if __name__ == '__main__':
    unittest.main()