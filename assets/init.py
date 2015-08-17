#!/usr/bin/python

import fileinput
import sys
import os
import shutil
import re


ACTIVEMQ_HOME = "/opt/activemq"
ACTIVEMQ_CONF = ACTIVEMQ_HOME + '/conf.tmp'






def replace_all(file, searchRegex, replaceExp):
  """ Replace String in file with regex
  :param file: The file name where you should to modify the string
  :param searchRegex: The pattern witch must match to replace the string
  :param replaceExp: The string replacement
  :return:
  """

  regex = re.compile(searchRegex, re.IGNORECASE)

  f = open(file,'r')
  out = f.readlines()
  f.close()

  f = open(file,'w')

  for line in out:
      if regex.search(line) is not None:
        line = regex.sub(replaceExp, line)

      f.write(line)

  f.close()


def add_end_file(file, line):
    """ Add line at the end of file

    :param file: The file where you should to add line to the end
    :param line: The line to add in file
    :return:
    """
    with open(file, "a") as myFile:
        myFile.write("\n" + line + "\n")



def do_setting_activemq_users(login, password):
    global ACTIVEMQ_HOME

    if login is None or login == "" :
        raise Exception("You must set the login")
    if password is None or password == "":
        raise Exception("You must set the password")

    add_end_file(ACTIVEMQ_CONF + "/users.properties", login + "=" + password)

def do_remove_default_account():
    global ACTIVEMQ_HOME


    replace_all(ACTIVEMQ_CONF + "/users.properties","admin=admin", "")
    replace_all(ACTIVEMQ_CONF + "/jetty-realm.properties", "admin: admin, admin", "")
    replace_all(ACTIVEMQ_CONF + "/jetty-realm.properties", "user: user, user", "")
    replace_all(ACTIVEMQ_CONF + "/groups.properties", "admins=admin", "")
    replace_all(ACTIVEMQ_CONF + "/jmx.access", "admin readwrite", "")
    replace_all(ACTIVEMQ_CONF + "/jmx.password", "admin activemq", "")
    replace_all(ACTIVEMQ_CONF + "/credentials.properties", "activemq\.username=system", "")
    replace_all(ACTIVEMQ_CONF + "/credentials.properties", "activemq\.password=manager", "")
    replace_all(ACTIVEMQ_CONF + "/credentials.properties", "guest\.password=password", "")



def do_setting_activemq_credential(user, password):
    global ACTIVEMQ_HOME

    if user is None or user == "" :
	raise Exception("You must set the user")

    if password is None or password == "" :
	raise Exception("You must set the password")

    add_end_file(ACTIVEMQ_CONF + "/credentials.properties", "activemq.username=" + user)
    add_end_file(ACTIVEMQ_CONF + "/credentials.properties", "activemq.password=" + password)



def do_setting_activemq_groups(group, users):
    global ACTIVEMQ_HOME

    if group is None or group == "" :
        raise Exception("You must set the group")

    if users is None:
        add_end_file(ACTIVEMQ_CONF + "/groups.properties", group + "=")
    else:
        add_end_file(ACTIVEMQ_CONF + "/groups.properties", group + "=" + users)


def do_setting_activemq_web_access(role, user, password):
    global ACTIVEMQ_HOME

    if role is None or role == "":
        raise Exception("You must set the role")

    if user is None or user == "":
        raise Exception("You must set the username")

    if password is None or password == "":
        raise Exception("You must set the password")


    add_end_file(ACTIVEMQ_CONF + "/jetty-realm.properties", user + ": " + password + ", " +role);


def do_setting_activemq_jmx_access(role, user, password):
    global ACTIVEMQ_HOME

    if role is None or role == "":
        raise Exception("You must set role")

    if user is None or user == "":
        raise Exception("You must set user")

    if password is None or password == "":
        raise Exception("You must set password")

    add_end_file(ACTIVEMQ_CONF + "/jmx.access", user + " " + role)
    add_end_file(ACTIVEMQ_CONF + "/jmx.password", user + " " + password)


def do_setting_activemq_log4j(loglevel):
    global ACTIVEMQ_HOME

    if loglevel is None or loglevel == "":
        raise Exception("You must set loglevel")

    replace_all(ACTIVEMQ_CONF + "/log4j.properties", "log4j\.rootLogger=[^,]+", "log4j.rootLogger=" + loglevel)
    replace_all(ACTIVEMQ_CONF + "/log4j.properties", "log4j\.logger\.org\.apache\.activemq\.audit=[^,]+", "log4j.logger.org.apache.activemq.audit=" + loglevel)


def do_setting_activemq_main(name, messageLimit, storageUsage, tempUsage, maxConnection, frameSize, topics, queues, enabledScheduler):

    if name is None or name == "":
        raise Exception("You must set the name")

    if messageLimit is None or messageLimit < 0:
        raise Exception("You must set the messageLimit")

    if storageUsage is None or storageUsage == "":
        raise Exception("You must set the storageUsage")

    if tempUsage is None or tempUsage == "":
        raise Exception("You must set the tempStorage")

    if maxConnection is None or maxConnection < 0:
        raise Exception("You must set the maxConnection")

    if frameSize is None or frameSize < 0:
        raise Exception("You must set the frameSize")

    replace_all(ACTIVEMQ_CONF + "/activemq.xml", 'brokerName="[^"]*"', 'brokerName="' + name + '"')
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", '<constantPendingMessageLimitStrategy limit="\d+"/>', '<constantPendingMessageLimitStrategy limit="' + str(messageLimit) + '"/>')
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", '<storeUsage limit="[^"]+"/>', '<storeUsage limit="' + storageUsage + '"/>')
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", '<tempUsage limit="[^"]+"/>', '<tempUsage limit="' + tempUsage + '"/>')
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", '\?maximumConnections=1000', "?maximumConnections=" + str(maxConnection))
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", 'wireFormat\.maxFrameSize=104857600', "wireFormat.maxFrameSize=" + str(frameSize))

    # Look for enabled scheduler
    if enabledScheduler is not None and enabledScheduler == "true" :
    	replace_all(ACTIVEMQ_CONF + "/activemq.xml", '<broker', '<broker schedulerSupport="true"')

    # We inject the setting to manage right on topic and queue
    rightManagement = """<plugins>
      		             <!--  use JAAS to authenticate using the login.config file on the classpath to configure JAAS -->
      		             <jaasAuthenticationPlugin configuration="activemq" />
		                 <authorizationPlugin>
        		            <map>
          			            <authorizationMap>
            				        <authorizationEntries>
              					        <authorizationEntry queue=">" read="admins,reads,writes,owners" write="admins,writes,owners" admin="admins,owners" />
              					        <authorizationEntry topic=">" read="admins,reads,writes,owners" write="admins,writes,owners" admin="admins,owners" />
              					        <authorizationEntry topic="ActiveMQ.Advisory.>" read="admins,reads,writes,owners" write="admins,reads,writes,owners" admin="admins,reads,writes,owners"/>
            				        </authorizationEntries>

            				        <!-- let's assign roles to temporary destinations. comment this entry if we don't want any roles assigned to temp destinations  -->
            				        <tempDestinationAuthorizationEntry>
              					        <tempDestinationAuthorizationEntry read="tempDestinationAdmins" write="tempDestinationAdmins" admin="tempDestinationAdmins"/>
           				            </tempDestinationAuthorizationEntry>
          			            </authorizationMap>
        		            </map>
      		             </authorizationPlugin>
	                     </plugins>\n"""
    replace_all(ACTIVEMQ_CONF + "/activemq.xml", '</broker>', rightManagement + '</broker>')



    if (topics is not None and topics != "") or (queues is not None and queues != ""):
        staticRoute = "<destinations>\n"
        if topics is not None and topics != "" :
            topicList = topics.split(';')
            for topic in topicList:
                staticRoute += '<topic physicalName="' + topic + '" />' + "\n"

        if queues is not None and queues != "":
            queueList = queues.split(';')
            for queue in queueList:
                staticRoute += '<queue physicalName="' + queue + '" />' + "\n"

        staticRoute += "</destinations>\n"

        replace_all(ACTIVEMQ_CONF + "/activemq.xml", '</broker>', staticRoute + '</broker>')

def do_setting_activemq_wrapper(minMemoryInMB, maxMemoryInMb):

    if minMemoryInMB is None or minMemoryInMB < 0:
        raise Exception("You must set the minMemory")

    if maxMemoryInMb is None or maxMemoryInMb < 0:
        raise Exception("You must set the maxMemory")

    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/wrapper.conf", "#?wrapper\.java\.initmemory=\d+", 'wrapper.java.initmemory=' + str(minMemoryInMB))
    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/wrapper.conf", "#?wrapper\.java\.maxmemory=\d+", 'wrapper.java.maxmemory=' + str(maxMemoryInMb))


def do_init_activemq():

    # We change the activemq launcher to start activemq with activmq user
    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/activemq", "#RUN_AS_USER=", "RUN_AS_USER=activemq")

    # We change some macro on wrapper.conf to move data
    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/wrapper.conf" ,"set\.default\.ACTIVEMQ_DATA=%ACTIVEMQ_BASE%\/data", "set.default.ACTIVEMQ_DATA=/data/activemq")
    
    # Fix bug #4 "Cannot mount a custom activemq.xml"
    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/wrapper.conf" ,"set\.default\.ACTIVEMQ_CONF=%ACTIVEMQ_BASE%/conf$", "set.default.ACTIVEMQ_CONF=%ACTIVEMQ_BASE%/conf.tmp")

    # We replace the log output
    replace_all(ACTIVEMQ_CONF + "/log4j.properties", "\$\{activemq\.base\}\/data\/", "/var/log/activemq/")
    replace_all(ACTIVEMQ_HOME + "/bin/linux-x86-64/wrapper.conf" ,"wrapper\.logfile=%ACTIVEMQ_DATA%\/wrapper\.log", "wrapper.logfile=/var/log/activemq/wrapper.log")


def setting_all():

    # First, we look if we must remove default account
    if os.getenv('ACTIVEMQ_REMOVE_DEFAULT_ACCOUNT') is not None and os.getenv('ACTIVEMQ_REMOVE_DEFAULT_ACCOUNT') == "true":
        do_remove_default_account()

    # Then we init some fix parameter
    do_init_activemq()


    # We setting the admin account
    if os.getenv('ACTIVEMQ_ADMIN_LOGIN') is not None and os.getenv('ACTIVEMQ_ADMIN_PASSWORD') is not None:
        do_setting_activemq_users(os.getenv('ACTIVEMQ_ADMIN_LOGIN'), os.getenv('ACTIVEMQ_ADMIN_PASSWORD'))
        do_setting_activemq_web_access("admin", os.getenv('ACTIVEMQ_ADMIN_LOGIN'), os.getenv('ACTIVEMQ_ADMIN_PASSWORD'))
        do_setting_activemq_groups("admins", os.getenv('ACTIVEMQ_ADMIN_LOGIN'))
	do_setting_activemq_credential(os.getenv('ACTIVEMQ_ADMIN_LOGIN'), os.getenv('ACTIVEMQ_ADMIN_PASSWORD'))

    # We keep the default admin user
    #else:
    #    do_setting_activemq_users("admin", "admin")
    #    do_setting_activemq_web_access("admin", "admin", "admin")

    # We setting the user account
    if os.getenv('ACTIVEMQ_USER_LOGIN') is not None and os.getenv('ACTIVEMQ_USER_PASSWORD') is not None:
        do_setting_activemq_users(os.getenv('ACTIVEMQ_USER_LOGIN'), os.getenv('ACTIVEMQ_USER_PASSWORD'))
        do_setting_activemq_web_access("user", os.getenv('ACTIVEMQ_USER_LOGIN'), os.getenv('ACTIVEMQ_USER_PASSWORD'))

    # We keep the default user
    #else:
    #    do_setting_activemq_users("user", "user")
    #    do_setting_activemq_web_access("user", "user", "user")

    # We setting the owner account
    if os.getenv('ACTIVEMQ_OWNER_LOGIN') is not None and os.getenv('ACTIVEMQ_OWNER_PASSWORD') is not None:
        do_setting_activemq_users(os.getenv('ACTIVEMQ_OWNER_LOGIN'), os.getenv('ACTIVEMQ_OWNER_PASSWORD'))
        do_setting_activemq_groups("owners", os.getenv('ACTIVEMQ_OWNER_LOGIN'))

    # We setting the writer account
    if os.getenv('ACTIVEMQ_WRITE_LOGIN') is not None and os.getenv('ACTIVEMQ_WRITE_PASSWORD') is not None:
        do_setting_activemq_users(os.getenv('ACTIVEMQ_WRITE_LOGIN'), os.getenv('ACTIVEMQ_WRITE_PASSWORD'))
        do_setting_activemq_groups("writes", os.getenv('ACTIVEMQ_WRITE_LOGIN'))

    # We setting the reader account
    if os.getenv('ACTIVEMQ_READ_LOGIN') is not None and os.getenv('ACTIVEMQ_READ_PASSWORD') is not None:
        do_setting_activemq_users(os.getenv('ACTIVEMQ_READ_LOGIN'), os.getenv('ACTIVEMQ_READ_PASSWORD'))
        if os.getenv('ACTIVEMQ_USER_LOGIN') is not None and os.getenv('ACTIVEMQ_USER_PASSWORD') is not None:
            do_setting_activemq_groups("reads", os.getenv('ACTIVEMQ_READ_LOGIN') + "," + os.getenv('ACTIVEMQ_USER_LOGIN'))
        else :
            do_setting_activemq_groups("reads", os.getenv('ACTIVEMQ_READ_LOGIN'))

    # We setting the JMX access
    if os.getenv('ACTIVEMQ_JMX_LOGIN') is not None and os.getenv('ACTIVEMQ_JMX_PASSWORD') is not None:
        do_setting_activemq_jmx_access("readwrite", os.getenv('ACTIVEMQ_JMX_LOGIN'), os.getenv('ACTIVEMQ_JMX_PASSWORD'))

    # We keep the default value
    #else:
    #    do_setting_activemq_jmx_access("readwrite", "admin", "activemq")

    # We setting the log level
    if os.getenv('ACTIVEMQ_LOGLEVEL') is not None:
        do_setting_activemq_log4j(os.getenv('ACTIVEMQ_LOGLEVEL'))

    # We keep the default value
    #else:
    #    do_setting_activemq_log4j("INFO")

    # We setting ActiveMQ
    if os.getenv('ACTIVEMQ_NAME') is None:
        name = "localhost"
    else:
        name = os.getenv('ACTIVEMQ_NAME')

    if os.getenv('ACTIVEMQ_PENDING_MESSAGE_LIMIT') is None:
        messageLimit = 1000
    else :
        messageLimit = os.getenv('ACTIVEMQ_PENDING_MESSAGE_LIMIT')

    if os.getenv('ACTIVEMQ_STORAGE_USAGE') is None:
        storageUsage = "100 gb"
    else:
        storageUsage = os.getenv('ACTIVEMQ_STORAGE_USAGE')

    if os.getenv('ACTIVEMQ_TEMP_USAGE') is None:
        tempUsage = "50 gb"
    else:
        tempUsage = os.getenv('ACTIVEMQ_TEMP_USAGE')

    if os.getenv('ACTIVEMQ_MAX_CONNECTION') is None:
        maxConnection = 1000
    else:
        maxConnection = os.getenv('ACTIVEMQ_MAX_CONNECTION')

    if os.getenv('ACTIVEMQ_FRAME_SIZE') is None:
        frameSize = 104857600
    else:
        frameSize = os.getenv('ACTIVEMQ_FRAME_SIZE')

    do_setting_activemq_main(name, messageLimit, storageUsage, tempUsage, maxConnection, frameSize, os.getenv('ACTIVEMQ_STATIC_TOPICS'), os.getenv('ACTIVEMQ_STATIC_QUEUES'), os.getenv('ACTIVEMQ_ENABLED_SCHEDULER'))

    # We setting wrapper
    if os.getenv('ACTIVEMQ_MIN_MEMORY') is None:
        minMemory = 128
    else:
        minMemory = os.getenv('ACTIVEMQ_MIN_MEMORY')

    if os.getenv('ACTIVEMQ_MAX_MEMORY') is None:
        maxMemory = 1024
    else:
        maxMemory = os.getenv('ACTIVEMQ_MAX_MEMORY')

    do_setting_activemq_wrapper(minMemory, maxMemory)




# We start the daemon
if(len(sys.argv) > 1 and sys.argv[1] == "start"):


    # We move all config file on temporary folder (Fix bug # 4)
    shutil.rmtree(ACTIVEMQ_CONF, ignore_errors=True);
    shutil.copytree(ACTIVEMQ_HOME + "/conf/", ACTIVEMQ_CONF); 

    # First we fix right on volume
    os.system("chown -R activemq:activemq /data/activemq")
    os.system("chown -R activemq:activemq " + ACTIVEMQ_CONF)
    os.system("chown -R activemq:activemq /var/log/activemq")

    # Then we generate on the flow the right setting
    setting_all()

    # To finish, we run supervisord to start ActiveMQ
    os.system("/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf")
