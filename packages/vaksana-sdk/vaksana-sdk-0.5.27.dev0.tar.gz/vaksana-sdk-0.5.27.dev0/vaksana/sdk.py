from __future__ import print_function

import sys
import random
import time

import os
import sys
import os.path
import ntpath
import signal
import weakref

import site;
pkg_dir = site.getsitepackages()
for d in pkg_dir:
    pd_vak = d + '/vaksana_proto'
    sys.path.insert(0, pd_vak)

import logging
from pykafka import KafkaClient

import grpc

from interceptors import consumer_interceptor
from interceptors import producer_interceptor

import vaksana_pb2
import vaksana_pb2_grpc
import intent_pb2
import intent_pb2_grpc
import mongo_pb2
import mongo_pb2_grpc
import ssl_pb2
import ssl_pb2_grpc
import stub_pb2
import stub_pb2_grpc

import ConfigParser
from utils.encrypt import (
        decrypt_rsa,
        sym_decrypt_resp,
        )

STORAGE_INTENT_NAME = 'storage'
KEYVAL_INTENT_NAME = 'keyval'

def clean_sdk_instances():
    for Vobj in vaksana.getinstances():
        Vobj.cleanup()

def signal_handler_int(sigid, frame):
    logging.info('Received: %d, Cleaning Vaksana SDK Instances' % (sigid,))
    clean_sdk_instances()
    sys.exit(signal.SIGINT)

def signal_handler_term(sigid, frame):
    logging.info('Received: %d, Cleaning Vaksana SDK Instances' % (sigid,))
    clean_sdk_instances()
    sys.exit(signal.SIGTERM)

def signal_handler_usr(sigid, frame):
    logging.info('Received: %d, Cleaning Vaksana SDK Instances' % (sigid,))
    clean_sdk_instances()
    sys.exit(0)

'''
    <summary>
        The class to interact with the market.

        Helps in:
            Producers :-
            ------------
            1. Registering a service (gRPC) to handle an intent.

            Consumers :-
            ------------
            1. Identifying the services which are available to handle an
               intent.
                - #TODO: Client can pass the test functions to validate
                - #TODO: Client can pass a storage to save the state (this
                  ensures interoperatability)
                - #TODO: Client can share the keys so the resources consumed
                  can be billed to the client directly.
            2. Host the service (as gRPC stub) based on the requirements.
    </summary>
'''
class vaksana(object):
    _instances = set()

    '''
    <summary>
        Initialises the Vaksana SDK. Expects the config file with
            - Phone Number
            - Email

        1. Initialises the Market Stub to user market functionality
        2. Loads or Exchange RSA Keys
        3. Exchange AES Keys for enrypted communication
        4. Registers the domain with the server
    </summary>
    '''
    def __init__(self, configfile):
        self._proto_urls = {}
        self._instances.add(weakref.ref(self))

        ''' Initialises a market stub for all the subsequent calls '''
        channel = grpc.insecure_channel('vaksana.com:8001')
        self.stub = vaksana_pb2_grpc.MarketStub(channel)
        self.vak_config = None
        self.log_topic = None
        #self.log_producer = None

        self.db_dict = {}

        config = ConfigParser.ConfigParser()
        config.read(configfile)
        self.rsa_file = config.get('VaksanaConnect', 'rsa')
        self.domain = config.get('VaksanaConnect', 'domain')
        self.usertype = config.get('VaksanaConnect', 'usertype')
        self.email = config.get('VaksanaConnect', 'email')
        self.phone = config.get('VaksanaConnect', 'phone')
        self.contact = vaksana_pb2.ContactDetails(phone=self.phone,
                                                   email=self.email)

        ''' Load/Exchange RSA Keys '''
        self.__load_rsa_key_pair()

        #Fetch AES Key for they session
        ''' Exchange AES Keys '''
        self.aes_key = self.__get_aes_key()

        ''' Registers the domain of the client & gets token in return for
            subsequent calls '''
        token = self.register_domain()
        self.token = vaksana_pb2.Token(token=token)

        self.void = vaksana_pb2.Void()

        #Things that need to be passed instead of Vaksana PEM file
        # 1. token
        # 2. AES Key

    def __del__(self):
        self.cleanup()

    def get_vaksana_config(self):
        self.vak_config = self.stub.GetConfig(self.void)

    def log(self, logstring):
        #TODO: Make Kafka part of the Market docker swarm and enable the
        #      logging using Kafka. Till then, disabled to avoid using another
        #      machine
        return

        if self.vak_config == None:
            self.get_vaksana_config()

        if self.log_topic == None:
            topic = self.token.token
            kafka_client = KafkaClient(hosts=self.vak_config.logurl)
            self.log_topic = kafka_client.topics[str(topic)]

        with self.log_topic.get_producer() as log_producer:
            log_producer.produce(logstring)

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def __get_key_from_skey(self, skey):
        enc_key = skey.key.key
        if skey.encrypted == True:
            signature=skey.key.signature
            cpvtkey=self.db_dict.get('pvtkey')
            spubkey=self.db_dict.get('serverpubkey')
            key = decrypt_rsa(cpvtkey, spubkey, enc_key, signature)
        else:
            key = enc_key

        return key

    '''
        <summary>
            In case RSA keys are already exchanges, it loads the keys.
            If the key file is missing or we are unable to load, it generates
            the new pair of keys.

            Private and Public keys are required to exchange the symmetric AES
            Key Only.

            #TODO: Make sure we double check with the user that the request is
            indeed sent by the user. So no one can keep calling this methon on
            user's behalf by mistake or intentionally.
        </summary>
    '''
    def __load_rsa_key_pair(self):
        if os.path.isfile(self.rsa_file):
            skey = self.stub.GetClientPubkey(self.contact)
            self.db_dict['pubkey'] = self.__get_key_from_skey(skey)
            f = open(self.rsa_file, 'rb')
            self.db_dict['pvtkey'] = f.read()
            f.close()
        else:
            skey = self.stub.GenerateRSAKeyPair(self.contact)
            print('Save the pem file shared in your mail')
            print('    and update the path in the configfile')
            sys.exit(1)

        skey = self.stub.GetPublicKey(self.contact)
        self.db_dict['serverpubkey'] = self.__get_key_from_skey(skey)
        return

    '''
        <summary>
            Its not possible to encrypt the communication with RSA (because of
            speed(?) and size constraints). To avoid, we use RSA to exchange
            the AES key in the begning which is used for rest of the
            communication in future.
        </summary>
    '''
    def __get_aes_key(self):
        skey = self.stub.GenerateAESKey(self.contact)
        try:
            key = self.__get_key_from_skey(skey)
            return key
        except Exception, e:
            print(str(e))
            print('Error in the private key. Remove it and exchange again')
            raise Exception('Invalid Key')
        return None

    '''
        <summary>
            Registers the client (domain) with the market.
            This will be eventually used for all the tracking and stats.

            Returns Token for all the subsequent queries.
        </summary>
    '''
    def register_domain(self):
        client_info = vaksana_pb2.ClientInfo(
                            contact_details=self.contact,
                            domain=self.domain,
                            usertype=self.usertype)
        stoken = self.stub.RegisterDomain(client_info)
        symen_token = stoken.token
        token = sym_decrypt_resp(self.aes_key, symen_token)
        return token

    '''
        <summary>
            Function to register an intent with the market.
        </summary>
    '''
    def register_container_intent(self, intent_name, proto_filepath, docker_url):
        #Signature Details
        proto_filename = ntpath.basename(proto_filepath)
        f = open(proto_filepath, 'rb')
        proto_content = f.read().encode('base64')
        f.close()
        proto_file = intent_pb2.Proto.File(
                filename=proto_filename,
                content=proto_content)

        proto = intent_pb2.Proto(proto=proto_file)

        #Container Details
        container = intent_pb2.Service.Container(
                url=docker_url)
        service = intent_pb2.Service(
                proto=proto,
                container=container)

        intent = intent_pb2.Intent(
                name=intent_name,
                service=service)

        cintent = vaksana_pb2.CIntent(
                token=self.token,
                intent=intent,
                encrypted=False)

        err = self.stub.RegisterIntent(cintent)
        return err

    def setup_mongo_intent_handler(self, docker_url='gargpankaj83/mongoclient'):
        sdk_proto_path = os.path.dirname(os.path.abspath(vaksana_pb2.__file__))
        mongo_proto_path = sdk_proto_path + '/mongo.proto'
        self.register_container_intent(STORAGE_INTENT_NAME,
                                       mongo_proto_path,
                                       docker_url)

    def setup_redis_intent_handler(self, docker_url='gargpankaj83/redisclient'):
        sdk_proto_path = os.path.dirname(os.path.abspath(vaksana_pb2.__file__))
        redis_proto_path = sdk_proto_path + '/redisclient.proto'
        self.register_container_intent(KEYVAL_INTENT_NAME,
                                       redis_proto_path,
                                       docker_url)

    def register_volume(self, volumes):
        vol_data = volumes.get('data')
        volume_data = stub_pb2.VolumeData(
                path=vol_data.get('path'),
                username=vol_data.get('username'),
                password=vol_data.get('password'))

        volume = stub_pb2.Volume(
                name=volumes.get('name'),
                docker_tag=volumes.get('docker_tag'),
                data=volume_data,
                bind=volumes.get('bind'),
                permissions=volumes.get('permissions', 'ro'))

        cvolume = vaksana_pb2.CVolume(
                token=self.token,
                volume=volume,
                encrypted=False)

        errcode = self.stub.RegisterVolume(cvolume)
        return errcode.err, errcode.msg

    def register_host(self, tag, hostname, cacert, certificate, publickey):
        docker_host = stub_pb2.DockerHost(
                tag=tag,
                hostname=hostname,
                cacert=cacert,
                cert=certificate,
                pubkey=publickey)

        cdocker_host = vaksana_pb2.CDockerHost(
                token = self.token,
                dockerhost = docker_host,
                encrypted = False)

        errcode = self.stub.RegisterHost(cdocker_host)
        return errcode.err, errcode.msg

    '''
        <summary>
            Given an intent, this launches the best suited handler.
            The url of the service is returned which can be used to initialise
            a (gRPC) stub.

            Server internally does the following
                - fetches a list of potential service handlers.
                - identifies the best service given the other constraints from
                  the consumer.

            #TODO: Client should be able to pass certain parameters here e.g.
                - Where the service must be hosted.
                - Test functions, etc
        </summary>
    '''
    def create_stub(self, intent_name, grpc_function,
                    docker_tag='', volume_name='',
                    storage_host='', storage_port=27017):
        intent = intent_pb2.Intent(
                name=intent_name)

        stub_details = stub_pb2.StubDetails(
                intent=intent,
                volume_name=volume_name,
                docker_tag=docker_tag)

        cstubdetails = vaksana_pb2.CStubDetails(
                token = self.token,
                stubdetails = stub_details,
                encrypted = False)

        surl = self.stub.CreateStub(cstubdetails)
        proto_url = surl.url
        service_id = surl.service_id
        service_token = surl.service_token.token
        service_aes_key = surl.service_aes_key

        self._proto_urls[proto_url] = (service_id,
                                       service_token,
                                       service_aes_key)

        qinterceptor = consumer_interceptor.consumer_interceptor(self)
        channel = grpc.insecure_channel(proto_url)
        #channel = grpc.intercept_channel(channel, qinterceptor)
        proto_stub = grpc_function(channel)

        ''' Waiting till the service is active '''
        while True:
            try:
                proto_stub.IsActive(self.void)
                break
            #TODO: Handle NotImplemented Exception and break from loop
            except Exception, e:
                logging.error(str(e))
                logging.info('Sleeping for 5s')
                time.sleep(5)

        #Generate Service Id
        server = vaksana_pb2.Server(hostname=storage_host, port=storage_port)
        service_id, service_token, service_aes_key = self._proto_urls[proto_url]
        token = vaksana_pb2.Token(token=service_token)
        credentials = vaksana_pb2.Credentials(service_token=token,
                                              service_id=service_id,
                                              service_aes_key=service_aes_key,
                                              server=server)
        proto_stub.SaveCredentials(credentials)

        return proto_url, proto_stub

    '''
        <summary>
            Either:
                - Cleans up a given service once its no longer required.
            Or:
                - Stops and Cleans up all the handlers which were hosted to get
                  the job done.
        </summary>
    '''
    def cleanup(self, proto_url=None):
        if proto_url:
            curl = vaksana_pb2.CUrl(
                    token=self.token,
                    url=proto_url,
                    encrypted=False)
            logging.info('Cleaning up stub related to %s' % (proto_url,))
            self.stub.DestroyStub(curl)
        else:
            logging.info('Cleaning up all stubs')
            for proto_url, (_id, _token, _aes) in self._proto_urls.iteritems():
                self.cleanup(proto_url=proto_url)


class vaksana_derived(vaksana):
    #TODO: Need to check if the token and keys are still valid
    def __init__(self, credentials):
        self.db_dict = {}

        self._proto_urls = {}
        self._instances.add(weakref.ref(self))

        ''' Initialises a market stub for all the subsequent calls '''
        channel = grpc.insecure_channel('vaksana.com:8001')
        self.stub = vaksana_pb2_grpc.MarketStub(channel)

        self.service_id = credentials.service_id

        ''' Token required for market calls '''
        token = credentials.service_token.token
        self.token = vaksana_pb2.Token(token=token)

        ''' AES Keys '''
        self.aes_key = credentials.service_aes_key

        self.void = vaksana_pb2.Void()

        ''' Kafka '''
        self.vak_config = None
        self.log_topic = None

    def get_storage_stub(self):
        url, storage_stub = self.create_stub(STORAGE_INTENT_NAME, mongo_pb2_grpc.MongoCStub)
        #channel = grpc.insecure_channel(url)
        #storage_stub = mongo_pb2_grpc.MongoCStub(channel)
        #self.wait_till_active(url, storage_stub)
        return storage_stub

if __name__ == '__main__':
    V = vaksana('client.cfg')
    #V.register_container_intent('vaksana.merge', 'DockerMerge')
    #intent = V.__find_service('vaksana.merge')
    #print(repr(intent))


