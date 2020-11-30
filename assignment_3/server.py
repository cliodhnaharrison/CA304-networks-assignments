#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import os
import socket
import sys
import threading

class Server(threading.Thread):

    def __init__(self, host, port):
        """
        Initialises the Server thread.

        Args:
            host (string): IP address of server
            port (int): port number of server
        """
        super().__init__()
        self.connections = defaultdict(list)
        self.host = host
        self.port = port


    def run(self):
        """
        Creates the listening socket. For each new connection, a ServerSocket thread
        is started to facilitate communications with that particular client.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print ("Listening at", sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            print ("Accepted next connection from {} to {}".format(sc.getpeername(), sc.getsockname()))

            # Client sends name of chatroom
            room_name = sc.recv(1024).decode('ascii')
            server_socket = ServerSocket(sc, sockname, room_name, self)
            server_socket.start()
            self.connections[room_name].append(server_socket)
            print ("Ready to receive messages from", sc.getpeername())

    def broadcast(self, message, source, room_name):
        """
        Sends the given message to all clients in the same room as the source
        except the source.

        Args:
            message (string): message to send
            source (tuple): tuple of host and port
            room_name (string): name of room that source is in
        """
        for connection in self.connections[room_name]:
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        """
        Removes the given connection from self.connections.

        Args:
            connection (ServerSocket): connection to be removed
        """
        self.connections[connection.room_name].remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, room_name, server):
        """
        Initialises the ServerSocket thread.

        Arg:
            sc (socket): socket object
            sockname (tuple): tuple of host and port
            room_name (string): name of room
            server (Server): server object where socket is running
        """
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.room_name = room_name
        self.server = server

    def run(self):
        """
        Receives data from connected client and broadcasts message to all other
        clients in that room.
        If the client has left the connection, closes the connected socket and
        removes itself from the list of threads in Server.
        """
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print("{} says {!r}".format(self.sockname, message))
                self.server.broadcast(message, self.sockname, self.room_name)
            else:
                print ("{} has closed the connection".format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        """
        Sends given message to connected server.

        Args:
            message (string): message to send
        """
        self.sc.sendall(message.encode('ascii'))


def exit(server):
    """
    Listens for 'q' to quit server.

    Args:
        server (Server): server object to listen to
    """
    while True:
        ipt = input('')
        if ipt == 'q':
            print ("Closing all connections...")
            for room in server.connections:
                for connection in server.connections[room]:
                    connection.sc.close()
            print ("Shutting down the server...")
            os._exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        ip = "0.0.0.0"
        port = 8080
    elif len(sys.argv) == 2:
        if "." in sys.argv.split(" ")[1]:
            ip = sys.argv.split(" ")[1]
            port = 8080
    else:
        ip = sys.argv[1]
        port = int(sys.argv[2])

    server = Server(ip, port)
    server.start()

    exit = threading.Thread(target = exit, args = (server,))
    exit.start()
