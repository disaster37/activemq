#!/usr/bin/with-contenv sh

cat << EOF > ${CONFD_HOME}/etc/conf.d/users.properties.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "users.properties.tmpl"
dest = "${APP_HOME}/conf/users.properties"
mode = "0600"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/users",
  "/admin"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/groups.properties.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "groups.properties.tmpl"
dest = "${APP_HOME}/conf/groups.properties"
mode = "0744"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/groups",
  "/admin"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/credentials.properties.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "credentials.properties.tmpl"
dest = "${APP_HOME}/conf/credentials.properties"
mode = "0600"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/admin"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/jetty-realm.properties.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "jetty-realm.properties.tmpl"
dest = "${APP_HOME}/conf/jetty-realm.properties"
mode = "0600"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/users",
  "/admin"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/log4j.properties.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "log4j.properties.tmpl"
dest = "${APP_HOME}/conf/log4j.properties"
mode = "0744"
gid = $GID
uid = $UID
keys = [
  "/logger"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/jmx.access.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "jmx.access.tmpl"
dest = "${APP_HOME}/conf/jmx.access"
mode = "0600"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/jmx"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/jmx.password.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "jmx.password.tmpl"
dest = "${APP_HOME}/conf/jmx.password"
mode = "0600"
gid = $GID
uid = $UID
keys = [
  "/config",
  "/jmx"
]
EOF

cat << EOF > ${CONFD_HOME}/etc/conf.d/activemq.xml.toml
[template]
prefix = "${CONFD_PREFIX_KEY}"
src = "activemq.xml.tmpl"
dest = "${APP_HOME}/conf/activemq.xml"
mode = "0744"
gid = $GID
uid = $UID
keys = [
  "/config"
]
EOF
