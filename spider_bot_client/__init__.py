import socket
import logging
import threading
import ctypes
import os
from spider_bot_client import types
from spider_bot_client import cmds


LOG = logging.getLogger(__name__)
HOST = os.environ.get('SB_HOST', '192.168.100.22')
PORT = int(os.environ.get('SB_PORT', 8888))
NOTIFY_PORT = int(os.environ.get('SB_NOTIFY_PORT', 8889))
MAX_PACKET_SIZE = 800


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.notify_thread = None
        self.notify_handler = None

    def get_state(self):
        # 1. send cmd
        self.sock.sendto(
            bytes(types.Header(cmd=cmds.CMD_GET_STATE, size=0)),
            self.server_address)
        # 2. recv data
        data, server = self.sock.recvfrom(4096)
        return types.GetStateRes.from_buffer_copy(data)

    def set_action(self, action, get_responce=False):
        # 1. send cmd
        cmd = types.SetActionCmd()
        cmd.header.cmd = cmds.CMD_SET_ACTION
        cmd.header.resp_flag = get_responce
        cmd.header.size = ctypes.sizeof(types.SetActionCmd) -\
            ctypes.sizeof(types.Header)
        cmd.action = action

        self.sock.sendto(
            bytes(cmd),
            self.server_address)

        if get_responce:
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return types.ResHeader.from_buffer_copy(data)

    def add_notify(self, port=NOTIFY_PORT, get_responce=False):
        if self.notify_thread is None:
            LOG.info('add_notify port:%s' % (port, ))
            # 1. create socket for listen
            self.notify_port = port
            self.notify_sock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.notify_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.notify_sock.bind(('0.0.0.0', port))

            # 2. create listen notify thread
            self.notify_thread = threading.Thread(target=self.listen_notify)
            self.notify_thread.start()

            # 3. send cmd
            cmd = types.AddNotifyCmd()
            cmd.header.cmd = cmds.CMD_ADD_NOTIFY
            cmd.header.resp_flag = get_responce
            cmd.header.size = ctypes.sizeof(types.AddNotifyCmd) -\
                ctypes.sizeof(types.Header)
            cmd.port = port
            print("add_notify port:", cmd.port)
            self.sock.sendto(
                bytes(cmd),
                self.server_address)

            if get_responce:
                # 4. recv data
                data, server = self.sock.recvfrom(4096)
                return types.ResHeader.from_buffer_copy(data)
        else:
            LOG.warning('notifier already exist')

    def rm_notify(self, get_responce=False):
        if self.notify_thread is not None:
            print('rm_notify port:%s' % (self.notify_port, ))
            # 1. stop thread
            # self.notify_sock.shutdown(socket.SHUT_RDWR)
            self.notify_sock.shutdown(socket.SHUT_RD)
            self.notify_thread.join()
            self.notify_sock = None
            self.notify_thread = None

            # 2. send cmd
            cmd = types.RmNotifyCmd()
            cmd.header.cmd = cmds.CMD_RM_NOTIFY
            cmd.header.resp_flag = get_responce
            cmd.header.size = ctypes.sizeof(types.RmNotifyCmd) -\
                ctypes.sizeof(types.Header)
            cmd.port = self.notify_port
            self.sock.sendto(
                bytes(cmd),
                self.server_address)

            if get_responce:
                # 2. recv data
                data, server = self.sock.recvfrom(4096)
                return types.ResHeader.from_buffer_copy(data)

    def manage_servo(self, cmd, address, limmit, get_responce=True):
        # 1. send cmd
        # print(cmd, address, limmit)
        packet = types.ManageServoCmd()
        packet.header.cmd = cmds.CMD_RM_NOTIFY
        packet.header.resp_flag = get_responce
        packet.header.size = ctypes.sizeof(packet) -\
            ctypes.sizeof(types.Header)
        packet.cmd = cmd
        packet.address = address
        packet.limmit = limmit

        self.sock.sendto(
            bytes(packet),
            self.server_address)

        if get_responce:
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return types.ManageServoRes.from_buffer_copy(data)

    def listen_notify(self):
        """handler for listen notifys from server"""
        try:
            LOG.info('listen_notify begin')
            while 1:
                data, addr = self.notify_sock.recvfrom(MAX_PACKET_SIZE)
                # process notify
                if self.notify_handler:
                    self.notify_handler(
                        types.GetStateRes.from_buffer_copy(data))
        except OSError:
            pass
        finally:
            LOG.info('listen_notify end')

    def close(self):
        # free socket and thread
        if self.notify_thread:
            self.rm_notify()
        self.sock.close()

    def set_leg_geometry(self, leg_num, leg_geometry, get_responce=False):
        cmd = types.SetLegGeometry()
        cmd.header.cmd = cmds.CMD_SET_LEG_GEOMETRY
        cmd.header.resp_flag = get_responce
        cmd.header.size = ctypes.sizeof(types.SetLegGeometry) -\
            ctypes.sizeof(types.Header)
        cmd.leg_num = leg_num
        cmd.geometry = leg_geometry

        self.sock.sendto(
            bytes(cmd),
            self.server_address)

        if get_responce:
            # 2. recv data
            data, server = self.sock.recvfrom(4096)
            return types.ResHeader.from_buffer_copy(data)
