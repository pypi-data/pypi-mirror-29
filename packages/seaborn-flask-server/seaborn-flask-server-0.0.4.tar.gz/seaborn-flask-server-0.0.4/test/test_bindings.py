import unittest, os
from example_flask_app.manager import main

BASE_DIR = '/'.join(os.path.abspath(__file__).replace('\\','/').split('/')[:-2])
XMPL_DIR = os.path.join(BASE_DIR, 'example_bindings')
TEST_DIR = os.path.join(BASE_DIR, 'example_flask_app',
                        'bindings','python_bindings')

class test_bindings(unittest.TestCase):

    def startTestRun(self):
        main()

    def compare_files(self, filename):
        with open(os.path.join(XMPL_DIR, filename), 'r') as fp:
            expected = fp.read()
        with open(os.path.join(TEST_DIR, filename), 'r') as fp:
            actual = fp.read()
        self.assertEqual(expected, actual)

    def test_connection(self):
        self.compare_files('connection.py')

    def test_account(self):
        self.compare_files('account.py')

    def test_account_access(self):
        self.compare_files('account_access.py')

    def test_account_transfer(self):
        self.compare_files('account_transfer.py')

    def test_echo(self):
        self.compare_files('echo.py')

    def test_user(self):
        self.compare_files('user.py')


if __name__ == '__main__':
    unittest.main()