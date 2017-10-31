FROM alpine:3.6
MAINTAINER Sebastien LANGOUREAUX (linuxworkgroup@hotmail.com)

# Application settings
ENV CONFD_PREFIX_KEY="/activemq" \
    CONFD_BACKEND="env" \
    CONFD_INTERVAL="60" \
    CONFD_NODES="" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    LANG="en_US.utf8" \
    APP_HOME="/opt/activemq" \
    APP_VERSION="5.15.2" \
    SCHEDULER_VOLUME="/opt/scheduler" \
    USER=activemq \
    GROUP=activemq \
    UID=10003 \
    GID=10003 \
    CONTAINER_NAME="alpine-activemq" \
    CONTAINER_AUHTOR="Sebastien LANGOUREAUX <linuxworkgroup@hotmail.com>" \
    CONTAINER_SUPPORT="https://github.com/disaster37/alpine-gocd-agent/issues" \
    APP_WEB="http://activemq.apache.org/"

# Install extra package
RUN apk --update add fping curl tar bash openjdk8-jre-base  &&\
    rm -rf /var/cache/apk/*

# Install confd
ENV CONFD_VERSION="0.14.0" \
    CONFD_HOME="/opt/confd"
RUN mkdir -p "${CONFD_HOME}/etc/conf.d" "${CONFD_HOME}/etc/templates" "${CONFD_HOME}/log" "${CONFD_HOME}/bin" &&\
    curl -Lo "${CONFD_HOME}/bin/confd" "https://github.com/kelseyhightower/confd/releases/download/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64" &&\
    chmod +x "${CONFD_HOME}/bin/confd"

# Install s6-overlay
RUN curl -sL https://github.com/just-containers/s6-overlay/releases/download/v1.19.1.1/s6-overlay-amd64.tar.gz \
    | tar -zx -C /


# Install ActiveMQ software
RUN \
    mkdir -p ${APP_HOME} /data /var/log/activemq  && \
    curl http://apache.mirrors.ovh.net/ftp.apache.org/dist/activemq/${APP_VERSION}/apache-activemq-${APP_VERSION}-bin.tar.gz -o /tmp/activemq.tar.gz &&\
    tar -xzf /tmp/activemq.tar.gz -C /tmp &&\
    mv /tmp/apache-activemq-${APP_VERSION}/* ${APP_HOME} &&\
    rm -rf /tmp/activemq.tar.gz &&\
    addgroup -g ${GID} ${GROUP} && \
    adduser -g "${USER} user" -D -h ${APP_HOME} -G ${GROUP} -s /bin/sh -u ${UID} ${USER}


ADD root /
RUN \
    chown -R ${USER}:${GROUP} ${APP_HOME} &&\
    chown -R ${USER}:${GROUP} /data &&\
    chown -R ${USER}:${GROUP} /var/log/activemq

# Expose all port
EXPOSE 8161
EXPOSE 61616
EXPOSE 5672
EXPOSE 61613
EXPOSE 1883
EXPOSE 61614

VOLUME ["/data", "/var/log/activemq"]
WORKDIR ${APP_HOME}
CMD ["/init"]