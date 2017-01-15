__author__ = 'langoureaux-s'


import os
import shutil
import unittest
import time
import sys
import stomp
from subprocess import Popen, PIPE

global_message = None
global_error = None


def run_cmd(cmd):
  p = Popen(cmd, stdout=PIPE, shell=True)
  output = p.communicate()[0]
  return (p.returncode, output)





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
        global global_error
        global global_message

        # Run ActiveMQ container
        rt,output = run_cmd(' /usr/bin/docker ps -f name=activemq')
        if rt == 0:
            print("Remove old ActiveMQ container")
            run_cmd('/usr/bin/docker stop activemq')
            run_cmd('/usr/bin/docker rm activemq')

        # Init global variables
        global_error = None
        global_message = None


    @classmethod
    def tearDown(self):


        # Stop and remove ActiveMQ container
        rt,output = run_cmd(' /usr/bin/docker ps -f name=activemq')
        if rt == 0:
            print("Remove old ActiveMQ container")
            run_cmd('/usr/bin/docker stop activemq')
            run_cmd('/usr/bin/docker rm activemq')

    def test_activemq_run(self):

        print("Start ActiveMQ")
        rt,output = run_cmd('/usr/bin/docker run -d --name activemq -p 61613:61613 webcenter/activemq:develop')
        if rt != 0:
            self.fail("Failed to start ActiveMQ container : %s" % output)
        time.sleep(60)

        rt,output = run_cmd(' /usr/bin/docker ps -f name=activemq')
        self.assertEqual(rt, 0, "ActiveMQ container not running")


    def test_activemq_run_default_option(self):
        """Check that activemq container start with default option"""
        global global_message
        global global_error

        print("Start ActiveMQ")
        rt,output = run_cmd('/usr/bin/docker run -d --name activemq -p 61613:61613 webcenter/activemq:develop')
        if rt != 0:
            self.fail("Failed to start ActiveMQ container : %s" % output)
        time.sleep(60)

        # Init stomp connexion
        conn = stomp.Connection([('172.17.0.1', 61613)])
        conn.set_listener('', MyListener())
        try:
          conn.start()
          # In default option, the topic and queue is not proctected
          conn.connect(wait=True)
          conn.subscribe(destination='/queue/test', id=1, ack='auto')

          self.assertEqual(global_error, None, "There are a error message")
          self.assertEqual(global_message, None, "There are a message")

          conn.send('/queue/test', 'test1')
          time.sleep(10)
          self.assertEqual(global_error, None, "There are a error message")
          self.assertEqual(global_message, 'test1', "Message not received")
        except Exception,e:
          self.fail("Connexion not work %s" % e)

        # Close stomp connexion
        conn.disconnect()


    def test_activemq_run_all_option(self):
        """Check that activemq container start with all option"""

        print("Start ActiveMQ")
        docker = '''
/usr/bin/docker run --name='activemq' -d -p 61613:61613 \
-e 'ACTIVEMQ_REMOVE_DEFAULT_ACCOUNT=true' \
-e 'ACTIVEMQ_ADMIN_LOGIN=admin' -e 'ACTIVEMQ_ADMIN_PASSWORD=admin_password' \
-e 'ACTIVEMQ_USER_LOGIN=test' -e 'ACTIVEMQ_USER_PASSWORD=test_password' \
-e 'ACTIVEMQ_OWNER_LOGIN=owner' -e 'ACTIVEMQ_OWNER_PASSWORD=owner_password' \
-e 'ACTIVEMQ_WRITE_LOGIN=producer' -e 'ACTIVEMQ_WRITE_PASSWORD=producer_password' \
-e 'ACTIVEMQ_READ_LOGIN=reader' -e 'ACTIVEMQ_READ_PASSWORD=reader_password' \
-e 'ACTIVEMQ_JMX_LOGIN=jmx' -e 'ACTIVEMQ_JMX_PASSWORD=jmx_password' \
-e 'ACTIVEMQ_LOGLEVEL=DEBUG' \
-e 'ACTIVEMQ_NAME=amqp-srv1' \
-e 'ACTIVEMQ_PENDING_MESSAGE_LIMIT=2000' \
-e 'ACTIVEMQ_STORAGE_USAGE=3 gb' -e 'ACTIVEMQ_TEMP_USAGE=1 gb' \
-e 'ACTIVEMQ_MAX_CONNECTION=10' \
-e 'ACTIVEMQ_FRAME_SIZE=1000000' \
-e 'ACTIVEMQ_STATIC_TOPICS=topic1;topic2;topic3' \
-e 'ACTIVEMQ_STATIC_QUEUES=queue1;queue2;queue3' \
-e 'ACTIVEMQ_MIN_MEMORY=64' -e  'ACTIVEMQ_MAX_MEMORY=128' \
-e 'ACTIVEMQ_ENABLED_SCHEDULER=true' \
-e 'ACTIVEMQ_ENABLED_AUTH=true' \
webcenter/activemq:develop
        '''
        rt,output = run_cmd(docker)
        if rt != 0:
            self.fail("Failed to start ActiveMQ container : %s" % output)
        time.sleep(60)

        # Init stomp connexion
        conn = stomp.Connection([('172.17.0.1', 61613)])
        conn.set_listener('', MyListener())

        try:
          conn.start()
          # In default option, the topic and queue is not proctected
          conn.connect('admin', 'admin_password', wait=True)
          conn.subscribe(destination='/queue/test', id=1, ack='auto')

          self.assertEqual(self.is_error(), False)
          self.assertEqual(self.is_message(), False)

          conn.send('/queue/test', 'test1')
          time.sleep(10)
          self.assertEqual(self.is_error(), False)
          self.assertEqual(self.is_message(), True)
        except Exception,e:
          self.fail("Connexion not work %s" % e)

        # Close stomp connexion
        conn.disconnect()
