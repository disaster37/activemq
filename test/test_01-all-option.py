__author__ = 'langoureaux-s'


import os
import shutil
import unittest
import time
import sys
import stomp


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
        self.error = message

    def on_message(self, headers, message):
        print('received a message "%s"' % message)
        self.message = message


    def is_message(self):
        if self.message is not None:
            return True
        else:
            return False

    def is_error(self):
        if self.error is not None:
            return True
        else:
            return False

class ActiveMQDockerTestCase(unittest.TestCase):
    """Tests for `Init.py`."""

    @classmethod
    def setUp(self):
        self.conn = stomp.Connection([('activemq', 62613)])
        self.conn.set_listener('', MyListener())
        self.conn.start()


    @classmethod
    def tearDown(self):
        self.conn.disconnect()


    def test_activemq_run_default_option(self):
        """Check that activemq container start with default option"""

        # In default option, the topic and queue is not proctected
        try:
          self.conn.connect('admin', 'admin', wait=True)
          self.conn.subscribe(destination='/queue/test', id=1, ack='auto')
        except Exception,e:
          self.fail("Connexion not work %s" % e)

        self.assertEqual(self.is_error(), False)
        self.assertEqual(self.is_message(), False)

        self.conn.send('/queue/test', 'test1')
        time.sleep(10)
        self.assertEqual(self.is_error(), False)
        self.assertEqual(self.is_message(), True)
