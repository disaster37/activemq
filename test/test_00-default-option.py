__author__ = 'langoureaux-s'


import os
import shutil
import unittest
import time
import sys
import stomp


global_message = None
global_error = None


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        global global_error
        print('received an error "%s"' % message)
        global_error = message

    def on_message(self, headers, message):
        global global_message
        print('received a message "%s"' % message)
        global_message = message


class ActiveMQDockerTestCase(unittest.TestCase):
    """Tests for `Init.py`."""

    @classmethod
    def setUp(self):
        self.conn = stomp.Connection([('activemq', 61613)])
        self.conn.set_listener('', MyListener())
        self.conn.start()


    @classmethod
    def tearDown(self):
        self.conn.disconnect()


    def test_activemq_run_default_option(self):
        """Check that activemq container start with default option"""
        global global_message
        global global_error

        # In default option, the topic and queue is not proctected
        try:
          self.conn.connect(wait=True)
          self.conn.subscribe(destination='/queue/test', id=1, ack='auto')
        except Exception,e:
          self.fail("Connexion not work %s" % e)

        self.assertEqual(global_error, None)
        self.assertEqual(global_message, None)

        self.conn.send('/queue/test', 'test1')
        time.sleep(10)
        self.assertEqual(global_error, None)
        self.assertEqual(global_message, 'test1')
