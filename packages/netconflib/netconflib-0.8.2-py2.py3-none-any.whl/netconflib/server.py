"""Server class.

This class listens to all the clients and processes incoming messages.
"""

import socket
import sys
import logging
from threading import Thread
from queue import Queue
import traceback
from .helper import get_my_ip
from .netconf import NetConf
from .commands import Commands
from .commands import Paths
from .gui import GUI

class Server:
    """This class provides server features
    and listens to all the clients.
    """

    def __init__(self, port):
        self.logger = logging.getLogger('app.netconflib.server')
        self.logger.info("Starting server...")

        # My ip address
        self.local_address = get_my_ip()

        self.ncl = NetConf(Paths.config_file)
        self.num_nodes = self.ncl.topology.get_nodes_count()

        self.threads = []
        self.result_q = Queue()
        self.is_active = True

        self.server_address = (get_my_ip(), port)

    def start_server(self):
        """Starts the server process which listens and accepts clients.
        """

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.logger.info("Socket created")

        # Bind the socket to the port
        self.logger.info('starting up on {} port {}'.format(*self.server_address))
        try:
            self.sock.bind(self.server_address)
        except:
            self.logger.error("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        # Listen for incoming connections
        self.sock.listen(self.num_nodes)
        self.logger.info("Server is now listening...")

        # infinite loop- do not reset for every requests
        while len(self.threads) < self.num_nodes:
            connection, address = self.sock.accept()
            ip, port = str(address[0]), str(address[1])
            self.logger.info("Connected with " + ip + ":" + port)

            try:
                t = Thread(target=self.client_thread, args=(connection, ip, port)).start()
                self.threads.append(t)
            except:
                print("Thread did not start.")
                traceback.print_exc()

        self.sock.close()
        self.logger.info("All client threads started.")
        self.start_gui()

    def client_thread(self, connection, ip, port, max_buffer_size=5120):
        """The client thread receives and processes client inputs.

        Arguments:
            connection {object} -- The connection to the client.
            ip {string} -- Client ip.
            port {integer} -- The port number.

        Keyword Arguments:
            max_buffer_size {integer} -- Buffer size for input (default: {5120})
        """

        while self.is_active:
            client_input = self.receive_input(connection, max_buffer_size)
            if "--QUIT--" in client_input:
                self.logger.info("Client is requesting to quit")
                connection.close()
                self.logger.info("Connection " + ip + ":" + port + " closed")
                self.is_active = False
            else:
                self.logger.info("Processed result: {}".format(client_input))

    def receive_input(self, connection, max_buffer_size):
        """Receives messages from the client connection.

        Arguments:
            connection {object} -- The connection to the client.
            max_buffer_size {integer} -- The max buffer size for input.

        Returns:
            string -- The processed result of the input.
        """

        try:
            client_input = connection.recv(max_buffer_size)
            client_input_size = sys.getsizeof(client_input)
        except ConnectionResetError:
            self.logger.error("Connection lost to the remote host.")
            connection.close()
            self.is_active = False
            return "--QUIT--"

        if client_input_size > max_buffer_size:
            self.logger.warning("The input size is greater than expected {}".format(
                client_input_size))
        decoded_input = client_input.decode(
            "utf8").rstrip()  # decode and strip end of line
        result = self.process_input(decoded_input)

        return result

    def process_input(self, input_str):
        """Process the client's input.
        
        Arguments:
            input_str {string} -- The input.
        
        Returns:
            string -- The result of the processing.
        """

        self.logger.info("Processing the input from the client...")
        result = ""
        for node in self.ncl.topology.nodes:
            if node.address in input_str:
                result = "Node {}".format(node.node_id)
                self.result_q.put(node.node_id + 1)
        return result

    def start_gui(self):
        """Starts the gui in main loop.
        Call this method only after starting the client threads.
        """

        g = GUI(self.result_q, self.num_nodes)
        g.run()
