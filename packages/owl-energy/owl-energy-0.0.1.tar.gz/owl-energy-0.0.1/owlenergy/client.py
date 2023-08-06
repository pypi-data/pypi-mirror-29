"""Module for handling connections to the OWL energy monitor

"""
import logging
import socket
import struct

logger = logging.getLogger(__name__)


class OWLClient(object):
    """ OWL Client for interacting with the OWL energy monitor.

        Args:
            host (str): the host to connect to the network OWL
            port (int): the port to connect to the network OWL
            multi_cast_address (str): the multi-cast address to listen to
            msg_buffer_size (int): the size of the socket message buffer

        Attributes:
            host (str): the host to connect to the network OWL
            port (int): the port to connect to the network OWL
            multi_cast_address (str): the multi-cast address to listen to
            msg_buffer_size (int): the size of the socket message buffer
            socket (obj): the socket for receiving data from the network OWL
        """

    def __init__(self, host='localhost', port=22600,
                 multi_cast_address='224.192.32.19', msg_buffer_size=512):

        self.host = host
        self.port = port
        self.multi_cast_address = multi_cast_address
        self.msg_buffer_size = msg_buffer_size
        self.socket = None

    def initialise_socket(self):
        """Public method to create and open a socket to the network OWL

        Returns:
            None
        """
        self.socket = self._create_socket()

    def get_reading(self):
        """Get an energy consumption reading

        This function reads data from the multi-cast socket and decodes it as
        utf-8.

        Returns:
            reading (str): xml representation of owl energy data
        """
        logger.info("Getting energy reading.")
        if self.socket is not None:
            reading = self.socket.recv(self.msg_buffer_size).decode('utf-8')
            return reading
        else:
            return None

    def _create_socket(self):
        """
        Creates a socket that listens to the OWL multi-cast.

        Creates and configures a socket that can listen to an OWL multi-cast.
        This uses the struct package to interact with the underlying C could to
        supply options.

        Returns:
            A socket that listens to the OWL multi-cast.
        """
        logger.info("Creating OWL socket.")
        # Create a new socket
        owl_socket = socket.socket(family=socket.AF_INET,
                                   type=socket.SOCK_DGRAM,
                                   proto=socket.IPPROTO_UDP)

        # Set the socket options
        owl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the local address and port
        owl_socket.bind((self.host, self.port))

        # Convert str to 4sl struct
        multi_req = struct.pack("4sl",
                                socket.inet_aton(self.multi_cast_address),
                                socket.INADDR_ANY)

        # Set socket options
        owl_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                              multi_req)

        return owl_socket

    def _destroy_socket(self):
        """Safely close the multi cast socket

        Returns:
            None
        """

        if self.socket is not None:
            self.socket.close()
            self.socket = None
