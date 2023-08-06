FROM centos:centos7
MAINTAINER Aditya Vaja <aditya.vaja@bigswitch.com>
RUN yum -y update && yum clean all
RUN yum groupinstall -y 'Development Tools'
RUN yum install -y epel-release
RUN yum install -y python-pbr
RUN yum install -y python-sphinx
RUN yum install -y ftp://195.220.108.108/linux/fedora/linux/releases/23/Everything/x86_64/os/Packages/p/python-oslo-sphinx-2.5.0-3.fc23.noarch.rpm
RUN yum install -y python-django
RUN yum install -y python2-devel
RUN yum install -y python-d2to1
RUN yum install -y python-lockfile
RUN yum install -y python-eventlet
RUN yum install -y python-six
RUN yum install -y python-netaddr
RUN yum install -y python-kombu
RUN yum install -y python-anyjson
RUN yum install -y python-iso8601
