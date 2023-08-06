#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .qonnection import Qonnection


class __Manager:
    """
    This object must never be used directly, because it is a singleton object.
    Usually, you do not need to make a connection yourself, but in case you do,
    you should use it like this:

    from aspic import manager
    connection = manager.qonnect((host, port))

    """
    def __init__(self):
        self._connections = {}

    def qonnect(self, address: tuple) -> Qonnection:
        """Use this method if your application uses Qt event loop"""
        if address not in self._connections:
            self._connections[address] = Qonnection(address)
        return self._connections[address]

    def disconnect(self, address: tuple) -> None:
        if address in self._connections:
            self._connections[address].close()
            del self._connections[address]

    def abort(self) -> None:
        for address in self._connections:
            self._connections[address].abort()

    connect = qonnect


manager = __Manager()
