# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import wx
from uuid import uuid4 as GUID
import math
try:
    from wx import SystemSettings_GetColour as GetColour
except ImportError:
    from wx import SystemSettings

    GetColour = SystemSettings.GetColour
from wx.lib import masked

REGISTER_PLUGIN = '''# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg

eg.RegisterPlugin(
{RegisterPlugin}
)


{ThreadClass}


class Text:
    # add variables with string that you want to be able to have translated
    # using the language editor in here
    {ActionText}


class {PluginName}(eg.PluginBase):
    text = Text

    # you want to add any variables that can be access from anywhere inside of
    # your plugin here
    def __init__(self):
        {AddAction}
{ThreadInit}

    # you will want to add any startup parameters and also run any startup code
    # here
    def __start__(self, *args):
{ThreadStart}

    # this gets called when eg is being closed and you can run code when that
    # happens
    def __close__(self):
        pass

    # this gets called as well when EG closes but it also gets called when a
    # plugin gets disabled. This is where you will do things like close any
    # open sockets
    def __stop__(self):
{ThreadStop}

    # You will replace the code in this method if you want to make a plugin
    # configuration dialog.
    def Configure(self, *args):
        eg.PluginBase.Configure(self, *args)


    # The next 2 are pretty self explanatory
    def OnComputerResume(self):
        pass

    def OnComputerSuspend(self):
        pass

    # This gets called when a plugin gets deleted from the tree. so here if
    # you use eg.PersistantData to store any data. that data needs to be
    # deleted when the plugin gets removed. this is where that gets done.
    def OnDelete(self):
        pass
{threadMethods}

{ActionClass}
'''

KIND_CHOICES = [
    'other',
    'remote',
    'external',
    'program'
]


add_action = 'self.AddAction(%s)'

action_text = '''
    class %s:
        name = %r
        description = 'Action %s'
'''

action_class = '''

class %s(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self, *args):
        pass

    # this is where you would put the code for an action configuration dialog
    def Configure(self, *args):
        text = self.text
        panel = eg.ConfigPanel()

        while panel.Affirmed():
            panel.SetResult()
'''


THREAD_STOP = '        self.plugin_thread.stop()'
THREAD_INIT = '        self.plugin_thread = ThreadClass(self)'
THREAD_START = '        self.plugin_thread.start(*args)'
THREAD_CLASS = '''
import threading # NOQA


class ThreadClass(object):
    def __init__(self, plugin):
        self.event = threading.Event()
        self.plugin = plugin
        self.args = None
        self.thread = None

    def start(self, *args):
        if self.thread is None:
            self.args = args
            self.thread = threading.Thread(name=__name__, target=self.run)

    def run(self):
        self.event.clear()
        while not self.event.isSet():
            # do your code here
            # if you need to wait use
            # self.event.wait(seconds)
            pass

        self.thread = None

    def stop(self):
        if self.thread is not None:
            self.event.set()
            self.thread.join(3)
'''

THREAD_ADDON = (
    THREAD_STOP,
    THREAD_INIT,
    THREAD_START,
    THREAD_CLASS
)

TCP_LISTEN_STOP = '        self.tcp_listen.stop()'
TCP_LISTEN_INIT = '        self.tcp_listen = TCPListen(self)'
TCP_LISTEN_START = '''        # You are going to need to make a config
        # dialog and add a port control
        self.tcp_listen.start(port)'''
TCP_LISTEN_CLASS = '''
import threading # NOQA
import socket # NOQA


class TCPListen(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._thread = None
        self._event = threading.Event()
        self.socks = []
        self.port = 0

    @property
    def interface_addresses(self, family=socket.AF_INET):
        for fam, a, b, c, sock_addr in socket.getaddrinfo('', None):
            if family == fam:
                yield sock_addr[0]

    def run(self):
        queue_lock = threading.Lock()
        queue = []
        queue_event = threading.Event()

        sock_threads = []
        def listen(address):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((address, self.port))
            sock.listen(3)

            self.socks.append(sock)

            while not self._event.isSet():
                try:
                    conn, addr = sock.accept()
                    data = conn.recv(4096)
                    try:
                        conn.close()
                    except socket.error:
                        pass

                    with queue_lock:
                        queue.append(data)
                        queue_event.set()

                except socket.error:
                    break
            try:
                sock.close()
            except socket.error:
                pass

            self.socks.remove(sock)
            sock_threads.remove(threading.currentThread())
            queue_event.set()

        for interface_address in self.interface_addresses:
            t = threading.Thread(target=listen, args=(interface_address,))
            sock_threads += [t]
            t.start()

        while sock_threads:
            queue_event.wait()

            with queue_lock:
                while queue:
                    queue_data = queue.pop(0)
                    self.plugin.process_data(queue_data)
                queue_event.clear()

        self._event.clear()
        self._thread = None

    def stop(self):
        if self._thread is not None:
            self._event.set()
            for sock in self.socks:
                try:
                    sock.close()
                except socket.error:
                    pass
            self._thread.join(3)

    def start(self, port):
        if self._thread is None:
            self.port = port
            self._thread = threading.Thread(target=self.run)
            self._thread.start()
'''
TCP_LISTEN_ADDON = (
    TCP_LISTEN_STOP,
    TCP_LISTEN_INIT,
    TCP_LISTEN_START,
    TCP_LISTEN_CLASS
)


TCP_SEND_STOP = '''        if self.sock is not None:
            try:
                self.sock.close()
            except socket.error:
                pass

            self.sock = None
'''
TCP_SEND_INIT = '''        self.sock = None
        self.port = None
        self.ip_address = None
'''
TCP_SEND_START = '''        # You are going to need to make a config
        # dialog and add a port control and an ip control
        self.ip_address = ip_address
        self.port = port
        self.sock = self.connect()
'''
TCP_SEND_METHOD = '''
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((self.ip_address, self.port))
        return sock

    def send(self, message):
        try:
            self.sock.sendall(message)
        except socket.error:
            self.sock = self.connect()
            self.send(message)

        # optional receive after sending the message

        try:
            data, addr = self.sock.recv(4096)
        except socket.error:
            data = None

        return data
'''

TCP_SEND_ADDON = (
    TCP_SEND_STOP,
    TCP_SEND_INIT,
    TCP_SEND_START,
    TCP_SEND_METHOD
)


MULTI_THREADED_TCP_STOP = '        self.tcp_server.stop()'
MULTI_THREADED_TCP_INIT = '        self.tcp_server = TCPServer(self)'
MULTI_THREADED_TCP_START = '''        # You are going to need to make a config
        # dialog and add a port control
        self.tcp_server.start(port)'''
MULTI_THREADED_TCP_CLASS = '''
import threading # NOQA
import socket # NOQA


class TCPConnection(threading.Thread):

    def __init__(self, handler, address, sock):
        self.handler = handler
        self.sock = sock
        self._event = threading.Event()
        threading.Thread.__init__(self, name=self.__name__ + '-' + address)

    def run(self):
        while not self._event.isSet():
            try:
                data = self.sock.recv(4096)
                self.handler.process_data(self, data)

            except socket.error:
                break

        self.sock = None
        self.handler.remove_connection(self)

    def send(self, message):
        if self.sock is not None:
            self.sock.sendall(message)

    def stop(self):
        if self.sock is not None:
            self._event.set()
            self.sock.close()
            self.join(1.0)

class TCPServer(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._thread = None
        self._event = threading.Event()
        self.socks = []
        self.connections = []
        self.port = 0
        self.queue_lock = threading.Lock()
        self.queue = []
        self.queue_event = threading.Event()

    @property
    def interface_addresses(self, family=socket.AF_INET):
        for fam, a, b, c, sock_addr in socket.getaddrinfo('', None):
            if family == fam:
                yield sock_addr[0]

    def run(self):


        sock_threads = []
        def listen(address):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((address, self.port))
            sock.listen(3)

            self.socks.append(sock)

            while not self._event.isSet():
                try:
                    conn, addr = sock.accept()
                    conn = TCPConnection(self, addr[0], conn)
                    self.connections.append(conn)
                    conn.start()
                except socket.error:
                    break
            try:
                sock.close()
            except socket.error:
                pass

            self.socks.remove(sock)
            sock_threads.remove(threading.currentThread())
            self.queue_event.set()

        for interface_address in self.interface_addresses:
            t = threading.Thread(target=listen, args=(interface_address,))
            sock_threads += [t]
            t.start()

        while sock_threads:
            self.queue_event.wait()
            with self.queue_lock:
                while queue:
                    client, queue_data = self.queue.pop(0)
                    self.plugin.process_data(client, queue_data)
                self.queue_event.clear()


        with self.queue_lock:
            del self.queue[:]

        self.queue_event.clear()
        self._event.clear()
        self._thread = None

    def remove_connection(self, sock):
        self.connections.remove(sock)

    def process_data(self, sock, data):
        with self.queue_lock:
            self.queue.append((sock, data))
            self.queue_event.set()

    def stop(self):
        if self._thread is not None:
            for conn in self.connections[:]:
                conn.stop()

            self._event.set()
            for sock in self.socks:
                try:
                    sock.close()
                except socket.error:
                    pass
            self._thread.join(3)

    def start(self, port):
        if self._thread is None:
            self.port = port
            self._thread = threading.Thread(target=self.run)
            self._thread.start()
'''

MULTI_THREADED_TCP_ADDON = (
    MULTI_THREADED_TCP_STOP,
    MULTI_THREADED_TCP_INIT,
    MULTI_THREADED_TCP_START,
    MULTI_THREADED_TCP_CLASS
)


UDP_SEND_STOP = '''        if self.sock is not None:
            try:
                self.sock.close()
            except socket.error:
                pass

            self.sock = None
'''
UDP_SEND_INIT = '''        self.sock = None
        self.port = None
        self.ip_address = None
'''
UDP_SEND_START = '''        # You are going to need to make a config
        # dialog and add a port control and an ip control
        self.ip_address = ip_address
        self.port = port
        self.sock = self.connect()
'''
UDP_SEND_METHOD = '''
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((self.ip_address, self.port))
        return sock

    def send(self, message):
        try:
            self.sock.sendall(message)
        except socket.error:
            self.sock = self.connect()
            self.send(message)

        # optional receive after sending the message

        try:
            data, addr = self.sock.recv(4096)
        except socket.error:
            data = ''

        return data
'''

UDP_SEND_ADDON = (
    UDP_SEND_STOP,
    UDP_SEND_INIT,
    UDP_SEND_START,
    UDP_SEND_METHOD
)

UDP_LISTEN_STOP = '        self.udp_listen.stop()'
UDP_LISTEN_INIT = '        self.udp_listen = UDPListen(self)'
UDP_LISTEN_START = '''        # You are going to need to make a config
        # dialog and add a port control
        self.udp_listen.start(port)'''
UDP_LISTEN_CLASS = '''
import threading # NOQA
import socket # NOQA


class UDPListen(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._thread = None
        self._event = threading.Event()
        self.socks = []
        self.port = 0

    @property
    def interface_addresses(self, family=socket.AF_INET):
        for fam, a, b, c, sock_addr in socket.getaddrinfo('', None):
            if family == fam:
                yield sock_addr[0]

    def run(self):
        queue_lock = threading.Lock()
        queue = []
        queue_event = threading.Event()

        sock_threads = []
        def listen(address):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((address, self.port))
            sock.listen(3)

            self.socks.append(sock)

            while not self._event.isSet():
                try:
                    conn, addr = sock.accept()
                    data = conn.recv(4096)

                    try:
                        conn.close()
                    except socket.error:
                        pass

                    with queue_lock:
                        queue.append(data)
                        queue_event.set()

                except socket.error:
                    break
            try:
                sock.close()
            except socket.error:
                pass

            self.socks.remove(sock)
            sock_threads.remove(threading.currentThread())
            queue_event.set()

        for interface_address in self.interface_addresses:
            t = threading.Thread(target=listen, args=(interface_address,))
            sock_threads += [t]
            t.start()

        while sock_threads:
            queue_event.wait()

            with queue_lock:
                while queue:
                    queue_data = queue.pop(0)
                    self.plugin.process_data(queue_data)
                queue_event.clear()

        self._event.clear()
        self._thread = None

    def stop(self):
        if self._thread is not None:
            self._event.set()
            for sock in self.socks:
                try:
                    sock.close()
                except socket.error:
                    pass
            self._thread.join(3)

    def start(self, port):
        if self._thread is None:
            self.port = port
            self._thread = threading.Thread(target=self.run)
            self._thread.start()
'''

UDP_LISTEN_ADDON = (
    UDP_LISTEN_STOP,
    UDP_LISTEN_INIT,
    UDP_LISTEN_START,
    UDP_LISTEN_CLASS
)


MULTI_THREADED_UDP_STOP = '        self.udp_server.stop()'
MULTI_THREADED_UDP_INIT = '        self.udp_server = UDPServer(self)'
MULTI_THREADED_UDP_START = '''        # You are going to need to make a config
        # dialog and add a port control
        self.udp_server.start(port)'''
MULTI_THREADED_UDP_CLASS = '''
import threading # NOQA
import socket # NOQA


class UDPConnection(threading.Thread):

    def __init__(self, handler, address, sock):
        self.handler = handler
        self.sock = sock
        self._event = threading.Event()
        threading.Thread.__init__(self, name=self.__name__ + '-' + address)

    def run(self):
        while not self._event.isSet():
            try:
                data = self.sock.recv(4096)
                self.handler.process_data(self, data)

            except socket.error:
                break

        self.sock = None
        self.handler.remove_connection(self)

    def send(self, message):
        if self.sock is not None:
            self.sock.sendall(message)

    def stop(self):
        if self.sock is not None:
            self._event.set()
            self.sock.close()
            self.join(1.0)

class UDPServer(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._thread = None
        self._event = threading.Event()
        self.socks = []
        self.connections = []
        self.port = 0
        self.queue_lock = threading.Lock()
        self.queue = []
        self.queue_event = threading.Event()

    @property
    def interface_addresses(self, family=socket.AF_INET):
        for fam, a, b, c, sock_addr in socket.getaddrinfo('', None):
            if family == fam:
                yield sock_addr[0]

    def run(self):


        sock_threads = []
        def listen(address):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((address, self.port))
            sock.listen(3)

            self.socks.append(sock)

            while not self._event.isSet():
                try:
                    conn, addr = sock.accept()
                    conn = TCPConnection(self, addr[0], conn)
                    self.connections.append(conn)
                    conn.start()
                except socket.error:
                    break
            try:
                sock.close()
            except socket.error:
                pass

            self.socks.remove(sock)
            sock_threads.remove(threading.currentThread())
            self.queue_event.set()

        for interface_address in self.interface_addresses:
            t = threading.Thread(target=listen, args=(interface_address,))
            sock_threads += [t]
            t.start()

        while sock_threads:
            self.queue_event.wait()
            with self.queue_lock:
                while queue:
                    client, queue_data = self.queue.pop(0)
                    self.plugin.process_data(client, queue_data)
                self.queue_event.clear()


        with self.queue_lock:
            del self.queue[:]

        self.queue_event.clear()
        self._event.clear()
        self._thread = None

    def remove_connection(self, sock):
        self.connections.remove(sock)

    def process_data(self, sock, data):
        with self.queue_lock:
            self.queue.append((sock, data))
            self.queue_event.set()

    def stop(self):
        if self._thread is not None:
            for conn in self.connections[:]:
                conn.stop()

            self._event.set()
            for sock in self.socks:
                try:
                    sock.close()
                except socket.error:
                    pass
            self._thread.join(3)

    def start(self, port):
        if self._thread is None:
            self.port = port
            self._thread = threading.Thread(target=self.run)
            self._thread.start()
'''

MULTI_THREADED_UDP_ADDON = (
    MULTI_THREADED_UDP_STOP,
    MULTI_THREADED_UDP_INIT,
    MULTI_THREADED_UDP_START,
    MULTI_THREADED_UDP_CLASS
)


TCP_CONNECTION_SERVER_STOP = '        self.server.stop()'
TCP_CONNECTION_SERVER_INIT = '        self.server = TCPServer(self)'
TCP_CONNECTION_SERVER_START = '''        # You are going to need to make a config
        # dialog and add a port control and an ip control
        self.server.start(ip, port)'''
TCP_CONNECTION_SERVER_CLASS = '''
import threading # NOQA
import socket # NOQA


class TCPListen(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self._thread = None
        self._event = threading.Event()
        self._send_event = threading.Event()
        self._send_lock = threading.Lock()
        self._sock = None
        self._ip = None
        self._port = None

    def send(self, msg):
        if self._sock is None:
            self.start(self, self._ip, self._port)

        with self._send_lock:
            self._send_result = None
            self._send_event.clear()
            self._sock.sendall(msg)
            self._send_event.wait(2.0)
            return self._send_result

    def run(self):
        self._sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        while not self._event.isSet():
            try:
                data = sock.recv(4096)
                if not self._send_event.isSet():
                    self._send_result = data
                    self._send_event.set()

               # do event code here for data

            except socket.error:
                pass
        try:
            sock.close()
        except socket.error:
            pass

        self._sock = None
        self._event.clear()
        self._thread = None

    def stop(self):
        if self._thread is not None:
            self._event.set()
            self._send_event.set()
            self._sock.shutdown(socket.SHUT_RDWR)
            self._thread.join(3)

    def start(self, ip, port):
        self._ip = ip
        self._port = port
        if self._thread is None:
            self._thread = threading.Thread(target=self.run)
            self._thread.start()


'''
TCP_CONNECTION_SERVER_ADDON = (
    TCP_CONNECTION_SERVER_STOP,
    TCP_CONNECTION_SERVER_INIT,
    TCP_CONNECTION_SERVER_START,
    TCP_CONNECTION_SERVER_CLASS
)


def PrettyPythonPrint(attrName, attrValue):
    types = (unicode, str)

    line = '    %s=' % attrName
    multiLine = len(line + repr(attrValue)) > 78

    if type(attrValue) in types and multiLine:
        line += '(\n'
        while '\n' in attrValue or len(attrValue) > 69:
            jump = attrValue.find('\n')
            if jump == -1 or jump > 69:
                jump = attrValue.find(' ')
                if 69 > jump > -1:
                    next_jump = attrValue.find(' ', jump + 1)
                    while 69 > next_jump > -1:
                        jump = next_jump
                        next_jump = attrValue.find(' ', jump + 1)

            line += ' ' * 8 + repr(attrValue[:jump + 1]) + '\n'
            attrValue = attrValue[jump + 1:]

        if attrValue:
            line += ' ' * 8 + repr(attrValue) + '\n'

        line = line[:-2] + '\n    ),\n'
    else:
        line += '%r,\n' % attrValue

    return line


def EqualizeWidths(*ctrls):
    maxWidth = max((ctrl.GetBestSize()[0] for ctrl in ctrls))
    for ctrl in ctrls:
        ctrl.SetMinSize((maxWidth, -1))


class SpinNumError(ValueError):
    _msg = ''

    def __init__(self, *args):
        if args:
            self._msg = self._msg.format(*args)

    def __str__(self):
        return self._msg


class MinValueError(SpinNumError):
    _msg = 'The set value {0} is lower then the minimum of {1}'


class MaxValueError(SpinNumError):
    _msg = 'The set value {0} is higher then the maximum of {1}'


class MinMaxValueError(SpinNumError):
    _msg = 'The minimum value {0} is higher the the max value {0}.'


class NegativeValueError(SpinNumError):
    _msg = 'The minimum value needs to be set when using negative values.'


class SpinNumCtrl(wx.Window):
    """
    A wx.Control that shows a fixed width floating point value and spin
    buttons to let the user easily input a floating point value.
    """

    def __init__(
        self,
        parent,
        id=-1,
        value=0,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TE_RIGHT,
        validator=wx.DefaultValidator,
        name="eg.SpinNumCtrl",
        min_val=0,
        max_val=100,
        allowNegative=False,
        groupDigits=False,
        fractionWidth=0,
        integerWidth=5,
        **kwargs
    ):

        limited = True
        groupChar = THOUSANDS_SEP
        decimalChar = DECIMAL_POINT
        self.increment = 1

        if max_val is None:
            max_val = (
                (10 ** integerWidth) -
                (10 ** -fractionWidth)
            )

        wx.Window.__init__(self, parent, id, pos, size, 0)
        self.SetThemeEnabled(True)
        numCtrl = masked.NumCtrl(
            parent=self,
            id=-1,
            value=value,
            pos=pos,
            size=size,
            style=style,
            validator=validator,
            name=name,
            allowNone=True,
            allowNegative=allowNegative,
            groupDigits=groupDigits,
            fractionWidth=fractionWidth,
            integerWidth=integerWidth,
            min=min_val,
            max=max_val,
            limited=limited,
            groupChar=groupChar,
            decimalChar=decimalChar,
        )
        self.numCtrl = numCtrl

        numCtrl.SetCtrlParameters(
            validBackgroundColour=GetColour(wx.SYS_COLOUR_WINDOW),
            emptyBackgroundColour=GetColour(wx.SYS_COLOUR_WINDOW),
            foregroundColour=GetColour(wx.SYS_COLOUR_WINDOWTEXT),
        )

        height = numCtrl.GetSize()[1]
        spinbutton = wx.SpinButton(
            self,
            -1,
            style=wx.SP_VERTICAL,
            size=(height * 2 / 3, height)
        )
        spinbutton.MoveBeforeInTabOrder(numCtrl)
        self.spinbutton = spinbutton
        numCtrl.Bind(wx.EVT_CHAR, self.OnChar)
        spinbutton.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        spinbutton.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)

        sizer = self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(numCtrl, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        sizer.Add(spinbutton, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(sizer)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        wx.CallAfter(numCtrl.SetSelection, -1, -1)

    def GetValue(self):
        return self.numCtrl.GetValue()

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.OnSpinUp(event)
            return
        if key == wx.WXK_DOWN:
            self.OnSpinDown(event)
            return
        event.Skip()

    def OnSetFocus(self, dummyEvent):
        self.numCtrl.SetFocus()
        self.numCtrl.SetSelection(-1, -1)

    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()

    def OnSpinDown(self, dummyEvent):
        value = self.numCtrl.GetValue() - self.increment
        self.SetValue(value)

    def OnSpinUp(self, dummyEvent):
        value = self.numCtrl.GetValue() + self.increment
        self.SetValue(value)

    def SetValue(self, value):
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        if value < 0 and not self.numCtrl.IsNegativeAllowed():
            value = 0
        res = self.numCtrl.SetValue(value)
        wx.PostEvent(self, eg.ValueChangedEvent(self.GetId(), value=value))
        return res

    def __OnSpin(self, pos):
        """
        This is the function that gets called in response to up/down arrow or
        bound spin button events.
        """

        # Ensure adjusted control regains focus and has adjusted portion
        # selected:
        numCtrl = self.numCtrl
        numCtrl.SetFocus()
        start, end = numCtrl._FindField(pos)._extent
        numCtrl.SetInsertionPoint(start)
        numCtrl.SetSelection(start, end)


class VersionCtrl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.NO_BORDER)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        major = wx.Choice(self, -1, choices=list(str(i) for i in range(10)))
        minor = wx.Choice(self, -1, choices=list(str(i) for i in range(10)))
        micro = wx.Choice(self, -1, choices=list(str(i) for i in range(10)))
        subset = wx.Choice(self, -1, choices=['', 'alpha', 'beta'])
        subset.SetSelection(1)
        major.SetSelection(0)
        minor.SetSelection(0)
        micro.SetSelection(1)

        dot1 = wx.StaticText(self, -1, '.')
        dot2 = wx.StaticText(self, -1, '.')

        sizer.Add(major, 0, wx.EXPAND)
        sizer.Add(dot1, 0, wx.ALIGN_BOTTOM | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(minor, 0, wx.EXPAND)
        sizer.Add(dot2, 0, wx.ALIGN_BOTTOM | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(micro, 0, wx.EXPAND)
        sizer.Add(subset, 0, wx.EXPAND)

        self.SetSizer(sizer)

        def get_value():
            ver = (
                str(major.GetStringSelection()) + '.' +
                str(minor.GetStringSelection()) + '.' +
                str(micro.GetStringSelection())
            )
            sub = subset.GetStringSelection()
            if sub:
                sub = sub[0]

            ver += sub
            return ver

        self.GetValue = get_value


class Frame(wx.Frame):

    ctrl = None
    frame = None

    def __init__(self):

        width = 80 * 6

        guid = '{' + str(GUID()).upper() + '}'

        wx.Frame.__init__(
            self,
            None,
            size=((width + 50) * 2, 900),
            title='Register Plugin Generator'
        )

        nameSt = wx.StaticText(self, -1, 'Name:')
        nameCtrl = wx.TextCtrl(self, -1, '')
        authorSt = wx.StaticText(self, -1, 'Author:')
        authorCtrl = wx.TextCtrl(self, -1, '')
        versionSt = wx.StaticText(self, -1, 'Version:')
        versionCtrl = VersionCtrl(self)
        descSt = wx.StaticText(self, -1, 'Description')
        descCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE, size=(width, 200))
        helpSt = wx.StaticText(self, -1, 'Help')
        helpCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE, size=(width, 200))
        urlSt = wx.StaticText(self, -1, 'URL:')
        urlCtrl = wx.TextCtrl(self, -1, '')
        hardwareSt = wx.StaticText(self, -1, 'Hardware Id\'s')
        hardwareCtrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE, size=(width, 200))
        kindSt = wx.StaticText(self, -1, 'Kind:')
        kindCtrl = wx.Choice(self, -1, choices=KIND_CHOICES)
        guidSt = wx.StaticText(self, -1, 'GUID:')
        guidCtrl = wx.TextCtrl(self, -1, guid, style=wx.TE_READONLY, size=(len(guid) * 7, 20))
        macroSt = wx.StaticText(self, -1, 'Create Macros:')
        macroCtrl = wx.CheckBox(self, -1, '')
        multiloadSt = wx.StaticText(self, -1, 'Can Multiload:')
        multiloadCtrl = wx.CheckBox(self, -1, '')

        iconSt = wx.StaticText(self, -1, 'Icon')
        iconCtrl = wx.TextCtrl(self, -1, 'None', style=wx.TE_MULTILINE, size=(width, 164))
        iconBaseSt = wx.StaticText(self, -1, 'Encode Icon:')
        iconBaseCtrl = wx.CheckBox(self, -1, '')

        action_st = wx.StaticText(self, -1, 'Action Names (comma separated):')
        action_ctrl = wx.TextCtrl(self, -1, '')

        thread_ctrl = wx.CheckBox(self, -1, 'Threading class')
        tcp_listen_ctrl = wx.CheckBox(self, -1, 'TCP socket listen')
        tcp_send_ctrl = wx.CheckBox(self, -1, 'TCP socket send')
        tcp_server_ctrl = wx.CheckBox(self, -1, 'Multi threaded TCP server')

        udp_listen_ctrl = wx.CheckBox(self, -1, 'UDP listen')
        udp_send_ctrl = wx.CheckBox(self, -1, 'UDP send')
        udp_server_ctrl = wx.CheckBox(self, -1, 'Multi threaded UDP server')
        threaded_socket_ctrl = wx.CheckBox(self, -1, 'Threaded TCP connection')

        EqualizeWidths(
            nameSt,
            authorSt,
            versionSt,
            descSt,
            helpSt,
            urlSt,
            hardwareSt,
            kindSt,
            guidSt,
            macroSt,
            multiloadSt,
            iconSt,
            iconBaseSt
        )

        kindCtrl.SetSelection(0)
        macroCtrl.SetValue(True)
        multiloadCtrl.SetValue(False)

        iconBaseSizer = wx.BoxSizer(wx.HORIZONTAL)
        iconBaseSizer.Add(iconBaseSt, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        iconBaseSizer.Add(iconBaseCtrl, 0, wx.EXPAND)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        middleSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        leftMultiSizer = wx.BoxSizer(wx.VERTICAL)
        rightMultiSizer = wx.BoxSizer(wx.VERTICAL)

        def OnView(evt):
            text = [
                ('name', unicode(nameCtrl.GetValue())),
                ('author', unicode(authorCtrl.GetValue())),
                ('version', unicode(versionCtrl.GetValue())),
                ('description', unicode(descCtrl.GetValue())),
                ('kind', unicode(kindCtrl.GetStringSelection())),
                ('url', unicode(urlCtrl.GetValue())),
                ('help', unicode(helpCtrl.GetValue())),
                ('canMultiLoad',multiloadCtrl.GetValue()),
                ('createMacrosOnAdd', macroCtrl.GetValue()),
                ('guid', unicode(guidCtrl.GetValue())),
                ('hardwareId', unicode(hardwareCtrl.GetValue())),
                (
                    'icon',
                    unicode(iconCtrl.GetValue())
                    if iconCtrl.GetValue() != 'None' else None
                )
            ]

            actions = action_ctrl.GetValue()
            if actions.strip():
                addActions = ''
                actionText = ''
                actionClass = ''

                for action in actions.split(','):
                    action = action.title().strip()
                    class_name = action.replace('-', '_').replace(' ', '_')
                    addActions += add_action % class_name + '\n        '
                    actionText += action_text % (class_name, action, action) + '\n    '
                    actionClass += action_class % class_name
            else:
                addActions = 'pass'
                actionText = 'pass'
                actionClass = ''

            threadClass = ''
            threadStart = ''
            threadInit = ''
            threadStop = ''
            threadMethods = ''

            for ctrl, templates in (
                (thread_ctrl, THREAD_ADDON),
                (tcp_listen_ctrl, TCP_LISTEN_ADDON),
                (tcp_send_ctrl, TCP_SEND_ADDON),
                (tcp_server_ctrl, MULTI_THREADED_TCP_ADDON),
                (udp_listen_ctrl, UDP_LISTEN_ADDON),
                (udp_send_ctrl, UDP_SEND_ADDON),
                (udp_server_ctrl, MULTI_THREADED_UDP_ADDON),
                (threaded_socket_ctrl, TCP_CONNECTION_SERVER_ADDON)
            ):
                if ctrl.GetValue():
                    stop, init, start, main_code = templates

                    if main_code in (TCP_SEND_METHOD, UDP_SEND_METHOD):
                        threadMethods += main_code
                    else:
                        threadClass += main_code

                    threadStart += start
                    threadInit += init
                    threadStop += stop

                    if addActions == 'pass':
                        addActions = ''

            if not threadStop:
                threadStop = '        pass'

            if not threadStart:
                threadStart = '        pass'

            formatted = dict(
                ThreadClass=threadClass,
                ThreadInit=threadInit,
                ThreadStart=threadStart,
                ThreadStop=threadStop,
                threadMethods=threadMethods,
                ActionClass=actionClass,
                ActionText=actionText,
                AddAction=addActions,
                RegisterPlugin=''.join(list(PrettyPythonPrint(*item) for item in text))[:-2],
                PluginName=str(text[0][1]).replace('-', '').replace(' ', '').strip()
            )

            text = REGISTER_PLUGIN.format(**formatted)

            if self.ctrl:
                self.ctrl.SetValue(text)
                self.frame.Show()
                self.frame.Raise()
            else:
                width = 80 * 6
                height = 700
                self.frame = wx.Frame(self, size=(width + 30, height + 30))
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.ctrl = wx.TextCtrl(
                    self.frame,
                    -1,
                    text,
                    size=(width, height),
                    style=wx.TE_MULTILINE | wx.TE_READONLY
                )

                def OnFrameClose(evt):
                    self.frame = None
                    self.ctrl = None
                    evt.Skip()

                self.frame.Bind(wx.EVT_CLOSE, OnFrameClose)
                sizer.Add(self.ctrl, 0, wx.EXPAND | wx.ALL, 10)
                self.frame.SetSizer(sizer)
                self.frame.Show()

            evt.Skip()

        def OnClose(evt):
            if self.frame:
                self.frame.Show(False)
                self.frame.Destroy()
            self.Show(False)
            self.Destroy()

        closeButton = wx.Button(self, -1, 'Close')
        viewButton = wx.Button(self, -1, 'View')
        closeButton.Bind(wx.EVT_BUTTON, OnClose)
        viewButton.Bind(wx.EVT_BUTTON, OnView)

        bSizer = wx.StdDialogButtonSizer()
        bSizer.Add(closeButton)
        bSizer.Add(viewButton)
        bSizer.Realize()

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((3, 3), 1)
        buttonSizer.Add(bSizer, 0, wx.TOP | wx.BOTTOM, 6)
        buttonSizer.Add((3, 3), 0)

        def LineSizer(sizer, *widgets):
            lineSizer = wx.BoxSizer(wx.HORIZONTAL)
            for i, widget in enumerate(widgets):
                if i + 1 == len(widgets):
                    args = (wx.EXPAND,)
                else:
                    args = (wx.EXPAND | wx.RIGHT, 20)
                lineSizer.Add(widget, 0, *args)
            sizer.Add(lineSizer, 0, wx.EXPAND | wx.ALL, 10)

        def MultiSizer(sizer, widget1, widget2):
            sizer.Add(widget1, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 10)
            sizer.Add(widget2, 0, wx.EXPAND | wx.ALL, 10)

        LineSizer(leftSizer, nameSt, nameCtrl)
        LineSizer(leftSizer, authorSt, authorCtrl)
        LineSizer(leftSizer, kindSt, kindCtrl)

        LineSizer(middleSizer, urlSt, urlCtrl)
        LineSizer(middleSizer, versionSt, versionCtrl)

        LineSizer(rightSizer, guidSt, guidCtrl)
        LineSizer(rightSizer, macroSt, macroCtrl)
        LineSizer(rightSizer, multiloadSt, multiloadCtrl)

        MultiSizer(leftMultiSizer, descSt, descCtrl)
        MultiSizer(leftMultiSizer, helpSt, helpCtrl)
        MultiSizer(rightMultiSizer, hardwareSt, hardwareCtrl)
        MultiSizer(rightMultiSizer, iconSt, iconCtrl)
        LineSizer(rightMultiSizer, iconBaseSizer)

        LineSizer(mainSizer, leftSizer, middleSizer, rightSizer)
        LineSizer(mainSizer, leftMultiSizer, rightMultiSizer)

        option_sizer = wx.BoxSizer(wx.HORIZONTAL)
        addon_sizer = wx.BoxSizer(wx.HORIZONTAL)

        tcp_sizer = wx.BoxSizer(wx.VERTICAL)
        udp_sizer = wx.BoxSizer(wx.VERTICAL)
        thread_sizer = wx.BoxSizer(wx.VERTICAL)

        tcp_sizer.Add(tcp_listen_ctrl, 0, wx.ALL, 5)
        tcp_sizer.Add(tcp_send_ctrl, 0, wx.ALL, 5)
        tcp_sizer.Add(tcp_server_ctrl, 0, wx.ALL, 5)

        udp_sizer.Add(udp_listen_ctrl, 0, wx.ALL, 5)
        udp_sizer.Add(udp_send_ctrl, 0, wx.ALL, 5)
        udp_sizer.Add(udp_server_ctrl, 0, wx.ALL, 5)

        thread_sizer.Add(thread_ctrl, 0, wx.ALL, 5)
        thread_sizer.Add(threaded_socket_ctrl, 0, wx.ALL, 5)

        addon_sizer.Add(tcp_sizer, 0, wx.EXPAND)
        addon_sizer.Add(udp_sizer, 0, wx.EXPAND)
        addon_sizer.Add(thread_sizer, 0, wx.EXPAND)

        option_sizer.Add(action_st, 0, wx.ALL, 5)
        option_sizer.Add(action_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(option_sizer, 0, wx.EXPAND)
        mainSizer.Add(addon_sizer, 0, wx.EXPAND)
        LineSizer(mainSizer, buttonSizer)

        self.SetSizer(mainSizer)


app = wx.GetApp()

if app is None:
    app = wx.App()
    locale = wx.Locale()
    THOUSANDS_SEP = locale.GetInfo(wx.LOCALE_THOUSANDS_SEP)
    DECIMAL_POINT = locale.GetInfo(wx.LOCALE_DECIMAL_POINT)

    frame = Frame()
    frame.Show()
    app.MainLoop()
else:
    locale = wx.Locale()
    THOUSANDS_SEP = locale.GetInfo(wx.LOCALE_THOUSANDS_SEP)
    DECIMAL_POINT = locale.GetInfo(wx.LOCALE_DECIMAL_POINT)

    frame = Frame()
    frame.Show()
