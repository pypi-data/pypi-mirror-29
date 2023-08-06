#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .const import Spec
from .qonnection import Qonnection


class Qommand(QtCore.QObject):
    sigFinished = QtCore.pyqtSignal(object)
    sigError = QtCore.pyqtSignal(str)

    def __init__(self, connection: Qonnection):
        super().__init__()
        self._serial = -1
        self._connection = connection
        self._message = self._connection.message
        self._connection.sigSpecReplyArrived.connect(self._parseReply)
        self._connection.sigConnectedToSpec.connect(self._register)
        if self._connection.connected:
            QtCore.QTimer.singleShot(0, self._register)

    def run(self, command: str):
        self._connection.send(self._message.command_run(command))
        self._serial = self._message.serial

    def _register(self):
        self._connection.send(self._message.command_register())

    def _parseReply(self, header, value):
        if self._serial != header.id:
            return
        if header.typ == Spec.Error:
            self.sigError.emit(str(value))
            return
        self._serial = -1
        self.sigFinished.emit(value)

    def __del__(self):
        self._connection.send(self._message.command_unregister())
