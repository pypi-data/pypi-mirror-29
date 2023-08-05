"""Micropede Client for Python"""

__version__ = '0.0.2'

import asyncio
import functools
import inspect
import json
import os
import time
import random
import re
import urllib
import uuid
from threading import Timer, Thread

import paho.mqtt.client as mqtt
from wheezy.routing import PathRouter
import pydash as _

from .api import Topics

DEFAULT_PORT = 1884
DEFAULT_TIMEOUT = 5000
_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')

def set_timeout(callback, timeout=DEFAULT_TIMEOUT):
    Timer(timeout/1000.0, callback).start()

def camel_to_snake(s):
    # https://gist.github.com/jaytaylor/3660565
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def get_class_name(self):
    safe_chars = '~@#$&()*!+=:;,.?/\''
    return urllib.parse.quote(camel_to_snake(self.__class__.__name__),
                              safe=safe_chars)


def get_receiver(payload):
    return _.get(payload, "__head__.plugin_name")


def wrap_data(key, value, name, version):
    msg = {}
    if (_.is_object(value) and value is not None):
        msg = value
    else:
        msg[key] = value

    _.set_(msg, "__head__.plugin_name", name)
    _.set_(msg, "__head__.plugin_version", version)

    return msg


def channel_to_route_path(channel):
    return channel


def channel_to_subscription(channel):
    return re.sub(r"\{(.+?)\}", "+", channel)


def generate_client_id(name, app_name, path='unknown'):
    return f'{name}>>{path}>>{app_name}>>{uuid.uuid1()}-{uuid.uuid4()}'

def safe(loop):
    def __safe(function):
        @functools.wraps(function)
        def _safe(*args, **kwargs):
            loop.call_soon_threadsafe(function, *args, **kwargs)
        return _safe
    return __safe

# Connection state
mqtt_cs_new = 0
mqtt_cs_connected = 1
mqtt_cs_disconnecting = 2
mqtt_cs_connect_async = 3


class MicropedeClient(Topics):
    """
       Python based client for Micropede Application Framework
       Used with the following broker:
       https://github.com/sci-bots/microdrop-3.0/blob/master/MoscaServer.js
    """

    def __init__(self, app_name, host="localhost", port=None, name=None,
                 version='0.0.0'):

        if (app_name is None):
            raise("app_name is undefined")

        if (port is None):
            port = 1884

        if (name is None):
            name = get_class_name(self)

        self.router = PathRouter()
        client_id = generate_client_id(name, app_name)
        self.__listen = _.noop

        self.app_name = app_name
        self.client_id = client_id
        self.name = name
        self.subscriptions = []
        self.host = host
        self.port = port
        self.version = version
        self.last_message = None
        self.loop = asyncio.get_event_loop()
        self.safe = safe(self.loop)
        self.wait_for = self.loop.run_until_complete
        self.client = None
        self.wait_for(self.connect_client(client_id, host, port))
    @property
    def is_plugin(self):
        return not _.is_equal(self.listen, _.noop)

    @property
    def listen(self):
        return self.__listen

    @listen.setter
    def listen(self, val):
        self.__listen = val

    def exit():
        pass

    def add_binding(self, channel, event, retain=False, qos=0, dup=False):
        return self.on(event, lambda d: self.send_message(
            channel, d, retain, qos, dup))

    def add_subscription(self, channel, handler):
        path = channel_to_route_path(channel)
        sub = channel_to_subscription(channel)
        route_name = f'{uuid.uuid1()}-{uuid.uuid4()}'
        future = asyncio.Future()

        try:
            if self.client._state != mqtt_cs_connected:
                if (future.done() == False):
                    future.set_exception(Exception(
                        f'Failed to add subscription. '+
                        +'Client is not connected {self.name}, {self.channel}'
                        ))
                return future

            def add_sub(*args, **kwargs):
                self.client.on_unsubscribe = _.noop
                def on_sub(client, userdata, mid, granted_qos):
                    self.client.on_subscribe = _.noop
                    if (future.done() == False):
                        future.set_result('done')
                self.client.on_subscribe = self.safe(on_sub)
                self.client.subscribe(sub)

            if sub in self.subscriptions:
                self.client.on_unsubscribe = self.safe(add_sub)
                self.client.unsubscribe(sub)
            else:
                self.subscriptions.append(sub)
                self.router.add_route(path, handler)
                add_sub()

        except Exception as e:
            if (future.done() == False):
                future.set_exception(e)

        return future

    def remove_subscription(self, channel):
        sub = channel_to_subscription(channel)
        future = asyncio.Future()

        def on_unsub(client, userdata, mid):
            self.client.on_unsubscribe = _.noop
            _.pull(self.subscriptions, sub)
            if (future.done() == False):
                future.set_result('done')

        self.client.unsubscribe(sub)
        return future

    def _get_subscriptions(self, payload, name):
        LABEL = f'{this.app_name}::get_subscriptions'
        return this.notify_sender(payload, this.subscriptions, 'get-subscriptions')

    def notify_sender(payload, response, endpoint, status='success'):
        if (satus != 'success'):
            response = _.flatten_deep(response)
        receiver = get_receiver(payload)
        if (receiver is not None):
            return receiver
        self.send_message(
            f'{this.app_name}/{this.name}/notify/{receiver}/{endpoint}',
            wrap_data(None, {'status': status, 'response': response},
                      self.name, self.version)
        )

        return response

    def connect_client(self, client_id, host, port, timeout=DEFAULT_TIMEOUT):
        self.client = mqtt.Client(client_id)
        future = asyncio.Future()

        def on_connect(client, userdata, flags, rc):
            if future.done():
                return

            self.subscriptions = []

            if self.is_plugin:
                def on_done_1(d):
                    def on_done_2(d):
                        if future.done():
                            return
                        self.listen()
                        self.default_sub_count = len(self.subscriptions)
                        self.client.on_disconnect = self.safe(self.exit)
                        future.set_result('done')

                    f2 = self.on_trigger_msg("exit", self.safe(self.exit))
                    f2.add_done_callback(self.safe(on_done_2))
                f1 = self.on_trigger_msg("get-subscriptions", self.safe(self._get_subscriptions))
                f1.add_done_callback(self.safe(on_done_1))
            else:
                self.listen()
                self.default_sub_count = 0
                if (future.done() == False):
                    future.set_result('done')

        self.client.on_connect = self.safe(on_connect)
        self.client.on_message = self.safe(self.on_message)
        self.client.connect(host=self.host, port=self.port)
        self.client.loop_start()

        def on_timeout():
            if (future.done() == False):
                future.set_exception(Exception(f'timeout {timeout}ms'))

        set_timeout(self.safe(on_timeout), timeout)
        return future

    def disconnect_client(self, timeout=DEFAULT_TIMEOUT):
        future = asyncio.Future()
        self.subscriptions = []
        self.router = PathRouter()

        def off():
            if hasattr(self, '_on_off_events'):
                del self._on_off_events

        if (_.get(self, 'client._state') != mqtt_cs_connected):
            off()
            if (hasattr(self, 'client')):
                del self.client
            future.set_result('done')
            return future
        else:
            def on_disconnect(*args, **kwargs):
                if future.done():
                    return
                off()
                if (hasattr(self, 'client')):
                    del self.client

                future.set_result('done')

            if hasattr(self, 'client'):
                self.client.on_disconnect = self.safe(on_disconnect)
                self.client.disconnect()
                set_timeout(self.safe(on_disconnect), timeout)
            else:
                if (future.done() == False):
                    future.set_result('done')

        return future

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
        except ValueError:
            print("Message contains invalid json")
            print(f'topic: {msg.topic}')
            payload = None

        topic = msg.topic
        if (topic is None or topic is ''):
            return

        method, args = self.router.match(topic)
        if method:
            method(payload, args)

    def send_message(self, topic, msg={}, retain=False, qos=0, dup=False, timeout=DEFAULT_TIMEOUT):
        future = asyncio.Future()
        if (_.is_dict(msg) and _.get(msg, '__head__') is None):
            head = wrap_data(None, None, self.name, self.version)['__head__']
            _.set_(msg, '__head__', head)
        message = json.dumps(msg)

        _mid = None
        def on_publish(client, userdata, mid):
            if (mid == _mid):
                if (future.done() == False):
                    future.set_result('done')

        def on_timeout():
            if (future.done() == False):
                future.set_exception(Exception(f'timeout {timeout}ms'))

        self.client.on_publish = self.safe(on_publish)
        (qos, _mid) = self.client.publish(topic, payload=message, qos=qos, retain=retain)
        set_timeout(self.safe(on_timeout), timeout)

        return future

    async def set_state(self, key, value):
        topic = f'{self.app_name}/{self.name}/state/{key}';
        await self.send_message(topic, value, True, 0, False)
