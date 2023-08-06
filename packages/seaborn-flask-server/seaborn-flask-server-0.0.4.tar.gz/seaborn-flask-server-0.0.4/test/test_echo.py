import os
import sys

flask_folder = os.path.abspath(__file__).replace('\\', '/').rsplit(
    '/flask_app', 1)[0]
sys.path.append(flask_folder)

from test.base import *


class EchoTest(BaseTest):
    def test_echo(self):
        ret = self.conn.echo.get()
        self.assertEquals("Hello Cruel World!", ret)

    def test_database_write(self):
        ret = self.conn.echo.key.post('test', 'passed')
        self.assertEquals({"echo_key": "test", "echo_value": "passed"}, ret)
        ret = self.conn.echo.key.get('test')
        self.assertEquals({"echo_key": "test", "echo_value": "passed"}, ret)
