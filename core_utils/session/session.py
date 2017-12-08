"""
    name : session.py
    
    purpose : all session related classes are inserted here.
    
    author : denjK
"""

import socket
import ssl
from abc import abstractmethod
from core_utils.logger import getLogger
from ssl_files import consts as ssl_file_consts

SSL_PROTOCOL = ssl.PROTOCOL_SSLv23


def create_ssl_socket(is_server, key_file=None, cert_file=None):
    """
    create an ssl socket (server or client) and returns it.
    :param bool is_server: is the socket a server or a client, if it is, key_file and cert_file is mandatory 
    :param key_file: the private key for the certificate
    :param cert_file: certificate for the server.
    :return SSLSocket: 
    """

    sock = socket.socket()
    ssl_sock = ssl.wrap_socket(sock, keyfile=key_file, certfile=cert_file, server_side=is_server,
                               cert_reqs=ssl.CERT_NONE, ssl_version=SSL_PROTOCOL)
    return ssl_sock


class SSLSocket(object):
    """ a basic implementation to an ssl socket"""

    SOCK_TIMEOUT = 15
    DEFAULT_BUFFER_LENGTH = 1024

    @abstractmethod
    def __init__(self, host, port):
        self._sock = None
        self._host = host
        self._port = port
        self._logger = getLogger("{0},{1}:{2}".format(self.__class__, host, port))

    def send_data(self, data):
        self._sock.send(data)

    def recv_data(self, buffer_length=DEFAULT_BUFFER_LENGTH):
        return self.recv_data(buffer_length)

    @classmethod
    def _convert_ssl_sock_to_SSLSocket(cls, sock):
        """
        create a new instance of cls as _sock is socket.
        :param socket.socket sock: a socket. 
        :return cls: an instance of the class.
        """
        host, port = sock.getsockname()
        ssl_sock = cls(host, port)
        ssl_sock._sock = sock
        return ssl_sock

    def set_timeout(self, seconds):
        self._sock.settimeout(seconds)

    def get_timeout(self):
        return self._sock.gettimeout()

    def shutdown(self):
        """
        shut both halves of the connection.
        """

        self._sock.shutdown(socket.SHUT_RDWR)


class SSLClient(SSLSocket):
    """ implementation of SSLClient """

    DEFAULT_BUFFER_LENGTH = 1024

    def __init__(self, host, port):
        super(SSLClient, self).__init__(host, port)
        self._sock = create_ssl_socket(False)
        self.set_timeout(self.SOCK_TIMEOUT)

    def connect(self):
        try:
            self._sock.connect((self._host, self._port))
            self._logger.info("Successfully connected to server!")
        except Exception as e:
            self._logger.fatal("Exception occurred! - {exc}".format(exc=e))
            raise e

    def send_data(self, data):
        self._sock.send(data)

    def recv_data(self, buffer_length=DEFAULT_BUFFER_LENGTH):
        try:
            return self._sock.recv(buffer_length)
        except ssl.SSLError as ssl_error:
            self._logger.critical(
                "Exception occurred when trying to receive data {exc}, returning empty string instead.".format(
                    exc=ssl_error))
            raise ssl_error

    def close(self):
        self._close()
        self._logger.info("SOCKET has been closed")

    def _close(self):
        self._sock.close()


class SSLServer(SSLSocket):
    """ implementation of SSLServer """

    DEFAULT_BACKLOG = 5

    def __init__(self, host, port, key_file=ssl_file_consts.PRIVATE_KEY, cert_file=ssl_file_consts.SERVER_CERTIFICATE):
        super(SSLServer, self).__init__(host, port)
        self._sock = create_ssl_socket(True,
                                       key_file=key_file,
                                       cert_file=cert_file)
        self.init()

    def init(self):
        """ initiation of starter command for the socket."""
        self._sock.bind((self._host, self._port))
        self._sock.listen(self.DEFAULT_BACKLOG)

    def accept(self):
        try:
            sock, (ip, port) = self._sock.accept()
            self._logger.info("accepted {ip},{port}".format(ip=ip, port=port))

            return SSLClient._convert_ssl_sock_to_SSLSocket(sock)
        except ssl.SSLError as e:
            self._logger.fatal("Exception occurred while accepting clients - {e}".format(e=e))

    def close(self):
        self._sock.close()
        self._logger.info("SOCKET has been closed")
