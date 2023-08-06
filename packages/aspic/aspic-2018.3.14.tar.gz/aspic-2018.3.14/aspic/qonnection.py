#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtNetwork
from . import logger
from .const import Spec
from .reply import Reply
from .message import Message


class Qonnection(QtCore.QObject):
    sigConnectedToSpec = QtCore.pyqtSignal()
    sigSpecReplyArrived = QtCore.pyqtSignal(object, object)
    sigError = QtCore.pyqtSignal(str)

    def __init__(self, address):
        """
        Spec address should be a tuple in one of the following form:
        (spec_host, tcp_port)  <- (str, int)
        (spec_host, spec_name) <- (str, str)
        """
        super().__init__()
        self._address = address
        self._aborting = False
        self._searching = False
        self._name = ''
        self._buf = b''
        self._connect()

    def _connect(self):
        host, port = self._address
        self._host = host
        try:
            self._port = int(port)
        except ValueError:
            self._searching = True
            self._port = Spec.MinPort
            self._name = port
        else:
            self._name = ''
            self._searching = False
        self._connectToSpec()

    def _connectToSpec(self):
        self._message = Message()
        self._reply = Reply()
        self._createSocket()
        self._sock.connectToHost(self._host, self._port)
        logger.info(f'Connecting to {self._host}:{self._port}')

    def send(self, msg: bytes):
        if self._sock.isValid():
            if self._buf:
                self._buf = self._buf[:self._sock.write(self._buf)]
            self._sock.write(msg)
        else:
            self._buf += msg

    # noinspection PyUnresolvedReferences
    def _createSocket(self):
        self._sock = QtNetwork.QTcpSocket()
        self._sock.setProxy(QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.NoProxy))
        self._sock.connected.connect(self._sayHello)
        self._sock.readyRead.connect(self._readResponse)
        self._sock.disconnected.connect(self._disconnected)
        self._sock.error.connect(self._serverHasError)

    def _sayHello(self):
        self.send(self._message.hello())

    def _setConnected(self, answer):
        if self._searching and answer == self._name:
            self._searching = False
            self._address = self._host, self._port
            logger.info(f'Found session "{self._name}" on {self._host}:{self._port}')
            return True
        if not self._searching:
            self._name = answer
            logger.info(f'Found session "{self._name}" on {self._host}:{self._port}')
            return True
        logger.info(f'Wrong session "{answer}" on {self._host}:{self._port}')
        return False

    def _searchNextPort(self):
        self._port += 1
        if self._port > Spec.MaxPort:
            self._port = Spec.MinPort
        QtCore.QTimer.singleShot(0, self._connectToSpec)

    def _readResponse(self):
        for header, answer in self._reply.unpack(bytes(self._sock.readAll())):
            if header.cmd == Spec.HelloReply:
                if self._setConnected(answer):
                    self.sigConnectedToSpec.emit()
                else:
                    self._searchNextPort()
            self.sigSpecReplyArrived.emit(header, answer)

    def _disconnected(self):
        if self._searching or self._port <= Spec.MaxPort:
            return
        s = f'The connection to {self._name} at {self._host}:{self._port} has been stopped'
        self.sigError.emit(s)
        logger.warning(s)
        self.reconnect()

    def reconnect(self):
        self._port = Spec.MaxPort
        self._searching = True
        QtCore.QTimer.singleShot(1000, self._searchNextPort)

    def _serverHasError(self):
        err = self._sock.errorString()
        if self._searching:
            logger.warning(f'Server error at {self._host}:{self._port}: {err}')
            self._searchNextPort()
        else:
            s = f'The server {self._name} at {self._host}:{self._port} has an error: {err}'
            self.sigError.emit(s)
            logger.error(s)
            self.reconnect()

    def close(self):
        self._searching = False
        self._sock.close()

    def __repr__(self):
        return f'<Qt SpecConnection to {self._name} running at {self._host}:{self._port}>'

    @property
    def connected(self):
        return self._sock.isValid() and not self._searching

    @property
    def name(self):
        return self._name

    @property
    def message(self):
        return self._message

    @property
    def address(self):
        return self._address

    def abort(self):
        if self._aborting:
            return
        self._aborting = True
        self.send(self._message.abort())
        self.sleep(100)
        self._aborting = False

    def sleep(self, msec):
        dieTime = QtCore.QTime.currentTime().addMSecs(msec)
        while QtCore.QTime.currentTime() < dieTime:
            QtCore.QCoreApplication.processEvents()
