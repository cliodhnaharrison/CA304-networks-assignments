#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import sys
import threading


class Client:
    def __init__(self, host, port, username, room):
        """
        Initialises Client object.

        Args:
            host (string): IP address of server
            port (int): port number of server
            username (string): username
            room (string): name of chatroom
        """

        self.host = host
        self.port = port
        self.username = username
        self.room = room
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """
        Establishes the server-client connection. Creates and starts the Send
        and Receive threads, and notifies other connected clients.
        """

        print ("Trying to connect to {}:{}...".format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print ("Successfully connected to {}:{}".format(self.host, self.port))
        self.sock.sendall(self.room.encode('ascii'))

        print ()
        print ('Welcome, {}! Getting ready to send and receive messages...'.format(self.username))

        send = Send(self.sock, self.username)
        receive = Receive(self.sock, self.username)

        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(self.username).encode("ascii"))
        print ("\rAll set! Leave the chatroom anytime by typing 'QUIT'\n")
        print ("{}: ".format(self.username), end = "")


class Send(threading.Thread):
    def __init__(self, sock, username):
        """
        Initialises Send thread. Sending thread listens for user input from the
        command line.

        Args:
            sock (socket): The connected ssocket object
            username (string): username
        """
        super().__init__()
        self.sock = sock
        self.username = username

    def run(self):
        """
        Listens for user input from command line and sends it to the server.
        Typing 'QUIT' will close the connection and exit.
        """
        while True:
            message = input('{}: '.format(self.username))

            if message == "QUIT":
                self.sock.sendall("Server: {} has left the chat.".format(self.username).encode('ascii'))
                break
            else:
                self.sock.sendall('{}: {}'.format(self.username, message).encode('ascii'))

        print ("\nQuitting...")
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):
    def __init__(self, sock, username):
        """
        Initialises Receive thread. Receiving thread listens for incoming messages
        from the server.

        Args:
            sock (socket): The connected ssocket object
            username (string): username
        """
        super().__init__()
        self.sock = sock
        self.username = username

    def run(self):
        """
        Receives data from the server and displays it in the terminal.
        Always listens for incoming data until either end has closed the socket.
        """
        while True:
            message = self.sock.recv(1024)
            if message:
                print ('\r{}\n{}: '.format(message.decode('ascii'), self.username), end = "")
            else:
                print ('\nOh no, we have lost connection to the server!')
                print ('\nQuitting...')
                self.sock.close()
                os._exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        username = sys.argv[1]
        ip = sys.argv[2]
        port = int(sys.argv[3])
        room = sys.argv[4]
        client = Client(ip, port, username, room)
        client.start()
    else:
        print ("Missing {} Arguments".format(5 - len(sys.argv)))
