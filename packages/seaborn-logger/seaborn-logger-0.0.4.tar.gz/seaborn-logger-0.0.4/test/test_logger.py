from seaborn.logger.logger import *
import unittest, requests

class test_logger():
    def test_request(self):
        log_file = os.path.join(os.path.split(__file__)[0], '_test.log')
        SeabornFormatter(
            relative_pathname="/seaborn/seaborn/"
        ).setup_logging(log_filename=log_file,
                        silence_modules=['requests'],
                        log_level='TRACE',
                        log_stdout_level='TRACE')
        
        msg = "Test: Hello World (Logger Worked)"
        log.trace(msg)
        test_exclusion = requests.get('http://google.com')
        logged_message = open(log_file, 'r').read()
        self.assertIn(msg,logged_message.strip(), 'Bad Log Message: %s' % logged_message)


if __name__ == '__main__':
    smoke_test()
