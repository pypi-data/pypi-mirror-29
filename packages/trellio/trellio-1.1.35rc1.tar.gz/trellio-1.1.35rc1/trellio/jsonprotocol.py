import asyncio
import json
import logging

from jsonstreamer import ObjectStreamer

from .sendqueue import SendQueue
from .utils.jsonencoder import TrellioEncoder


class JSONProtocol(asyncio.Protocol):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._send_q = None
        self._connected = False
        self._transport = None
        self._obj_streamer = None
        self._pending_data = []

    @staticmethod
    def _make_frame(packet):
        string = json.dumps(packet, cls=TrellioEncoder) + ','
        return string.encode()

    def is_connected(self):
        return self._connected

    def _write_pending_data(self):
        for packet in self._pending_data:
            frame = self._make_frame(packet)
            self._transport.write(frame)
        self._pending_data.clear()

    def connection_made(self, transport):
        self._connected = True
        self._transport = transport
        try:
            self._transport.send = self._transport.write
        except:
            pass
        self._send_q = SendQueue(transport, self.is_connected)
        self.set_streamer()
        self._send_q.send()

    def set_streamer(self):
        self._obj_streamer = ObjectStreamer()
        self._obj_streamer.auto_listen(self, prefix='on_')
        self._obj_streamer.consume('[')

    def connection_lost(self, exc):
        self._connected = False
        self.logger.info('Peer closed %s', self._transport.get_extra_info('peername'))

    def send(self, packet):
        frame = self._make_frame(packet)
        self._send_q.send(frame)
        self.logger.debug('Data sent: %s', frame.decode())

    def close(self):
        self._transport.write(']'.encode())  # end the json array
        self._transport.close()

    def data_received(self, byte_data):
        string_data = byte_data.decode()
        self.logger.debug('Data received: %s', string_data)
        try:
            self._obj_streamer.consume(string_data)
        except:
            # recover from invalid data
            self.logger.exception('Invalid data received')
            self.set_streamer()

    def on_object_stream_start(self):
        raise RuntimeError('Incorrect JSON Streaming Format: expect a JSON Array to start at root, got object')

    def on_object_stream_end(self):
        del self._obj_streamer
        raise RuntimeError('Incorrect JSON Streaming Format: expect a JSON Array to end at root, got object')

    def on_array_stream_start(self):
        self.logger.debug('Array Stream started')

    def on_array_stream_end(self):
        del self._obj_streamer
        self.logger.debug('Array Stream ended')

    def on_pair(self, pair):
        self.logger.debug('Pair {}'.format(pair))
        raise RuntimeError('Received a key-value pair object - expected elements only')


class TrellioProtocol(JSONProtocol):
    def __init__(self, handler):
        super(TrellioProtocol, self).__init__()
        self._handler = handler

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        self.logger.info('Connection from %s', peer_name)
        super(TrellioProtocol, self).connection_made(transport)

    def connection_lost(self, exc):
        super(TrellioProtocol, self).connection_lost(exc)
        try:
            self._handler._handle_connection_lost(self)
        except Exception as e:
            self.logger.exception(str(e))

    def on_element(self, element):
        try:
            self._handler.receive(packet=element, protocol=self, transport=self._transport)
        except:
            # ignore any unhandled errors raised by handler
            self.logger.exception('api request exception')
            pass
