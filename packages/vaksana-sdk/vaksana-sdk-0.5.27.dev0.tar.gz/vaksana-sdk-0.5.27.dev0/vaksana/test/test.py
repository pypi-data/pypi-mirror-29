import time
import grpc
import random
import logging

import certifi
import urllib3
import urllib3.contrib.pyopenssl

from vaksana.sdk import vaksana
from vakdocker.container import container

def test_ssl_keypair(V):
    a, b, c = V.get_ssl_keypair('client.vaksana.com')
    print a
    print b
    print c

def test_docker_start_stop(V):
    mongo_volumes = {}
    mongo_dcont = container.local_start_container('mongo:latest',
                                port_map={27017: 27017}, volumes=mongo_volumes)

    container.local_stop_container(mongo_dcont)

def test_docker_handler():
    dh = container('test.cfg', 'gargpankaj83/mongoclient')
    proto_url = dh.start_container()
    print proto_url
    dh.stop_container()

if __name__ == '__main__':
    urllib3.disable_warnings()
    logging.captureWarnings(True)

    #V = vaksana('test.cfg')
    #test_ssl_keypair(V)
    #test_docker_start_stop(V)
    test_docker_handler()
    #V.start_docker_daemon('keys', 'client.vaksana.com')
    #V.stop_docker_daemon()
