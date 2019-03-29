FROM ubuntu:trusty

ENV TOX_VERSION 3.8.3
ENV PYTHON_VERSIONS "2.7 3.4 3.5 3.6"
ENV GOSU_VERSION 1.11

RUN apt-get update
RUN apt-get upgrade -y

# install pythons, pypy, gosu
COPY install-pythons.sh install-gosu.sh /
# Install gosu to run tox as the "tox" user instead of as root.
# https://github.com/tianon/gosu#from-debian

RUN /bin/bash /install-pythons.sh \
 && /bin/bash /install-gosu.sh \
 && rm /*.sh

ENTRYPOINT ["tox"]

# temporarily separate tox install to speed up builds
COPY install-tox.sh tox.sh /
RUN /bin/bash /install-tox.sh \
 && rm /*.sh

# simple self-test (run as root and testuser)
COPY self-test.sh /
RUN /bin/bash /self-test.sh \
 && gosu testuser /bin/bash /self-test.sh \
 && rm /*.sh
