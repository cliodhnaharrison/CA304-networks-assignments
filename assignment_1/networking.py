#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import commonprefix

class IPAddress:
    def __init__(self, ip_dot_str, subnet_mask=None):
        """
        Initialises required attributes of an IP Address object.

        Args:
            ip_dot_str (str): An IP address in decimal dot notation
            subnet_mask (str): A subnet mask in decimal dot notation
                               (default is None)
        """

        # All the required attributes are calculated on initialisation by class
        # functions.
        self.ip_dot_str = ip_dot_str
        self.ip_class = self.what_class()
        self.prefix = self.what_prefix()
        self.network_bits = self.what_network_bits()
        self.host_bits = self.what_host_bits()
        self.num_networks = self.how_many_networks()
        self.num_hosts = self.how_many_hosts()
        self.first_address = self.what_first_address()
        self.last_address = self.what_last_address()
        self.subnet_mask = None

        # If a subnet mask is passed then the required attributes are calculated
        if subnet_mask:
            self.subnet_mask = subnet_mask
            self.cidr_notation = self.to_cidr_notation()
            self.num_subnets = self.how_many_subnets()
            self.addressable_hosts = self.how_many_addressable_hosts()
            self.valid_subnets = self.what_valid_subnets()
            self.broadcast_addresses = self.what_broadcast_addresses()
            self.subnet_firsts = self.what_subnet_firsts()
            self.subnet_lasts = self.what_subnet_lasts()


    def __str__(self):
        """
        Compiles a message of the stats of the IPAddress object based on whether
        there is a subnet mask.
        """
        message = ""
        if self.subnet_mask:
            message += f"Address: {self.cidr_notation}\n"
            message += f"Subnets: {str(self.num_subnets)}\n"
            message += f"Addressable hosts per subnet: {str(self.addressable_hosts)}\n"
            message += f"Valid subnets: {self.valid_subnets}\n"
            message += f"Broadcast addresses: {self.broadcast_addresses}\n"
            message += f"First addresses: {self.subnet_firsts}\n"
            message += f"Last addresses: {self.subnet_lasts}"
        else:
            message += f"Class: {self.ip_class}\n"
            message += f"Network: {str(self.num_networks)}\n"
            message += f"Host: {str(self.num_hosts)}\n"
            message += f"First address: {self.first_address}\n"
            message += f"Last address: {self.last_address}"
        return message


    def what_class(self):
        """
        Derives the class of an IP address.

        Returns:
            string: string of what class the IP is
        """
        # Dict where key is position of the first 0 in each class of IP
        class_blocks = {0: "A", 1: "B", 2: "C", 3: "D"}

        bin_ip_addr = to_binary_string(self.ip_dot_str)[0]

        # Loops through binary IP until it finds first zero to determine class
        for i in range(len(bin_ip_addr)):
            if bin_ip_addr[i] == "0":
                if i in class_blocks.keys():
                    return class_blocks[i]
                else:
                    return "E"

    def what_prefix(self):
        """
        Determines binary prefix of IP based on class.

        Returns:
            string: binary prefix of IP
        """
        prefixes = {"A": "0", "B": "10", "C": "110", "D": "1110", "E": "11110"}
        return prefixes[self.ip_class]


    def what_network_bits(self):
        """
        Determines network bits based on class.

        Returns:
            int: number of network bits
            or
            string: N/A if IP is class D or E
        """
        if self.ip_class == "A":
            return 7
        elif self.ip_class == "B":
            return 14
        elif self.ip_class == "C":
            return 21
        else:
            return "N/A"


    def what_host_bits(self):
        """
        Determines host bits based on class.

        Returns:
            int: number of host bits
            orfirst
            string: N/A if IP is class D or E
        """
        if self.ip_class == "A":
            return 24
        elif self.ip_class == "B":
            return 16
        elif self.ip_class == "C":
            return 8
        else:
            return "N/A"


    def how_many_networks(self):
        """
        Determines number of networks.

        Returns:
            int: number of networks
            or
            string: N/A if IP is class D or E
        """
        if self.network_bits == "N/A":
             return "N/A"
        else:
            return 2**self.network_bits


    def how_many_hosts(self):
        """
        Determines number of hosts.

        Returns:
            int: number of hosts
            or
            string: N/A if IP is class D or E
        """
        if self.host_bits == "N/A":
            return "N/A"
        else:
            return 2**self.host_bits


    def what_first_address(self):
        """
        Determines first address of a class.

        Returns:
            string: IP address in decimal dot notation
        """
        # Pad IP's prefix with 0's until string length is 8 in a list
        # Then add 3 lists each with 8 0's in them. Convert to decimal dot.
        return to_decimal_dot([self.prefix.ljust(8, "0")] + (["0" * 8] * 3))


    def what_last_address(self):
        """
        Determines last address of a class.

        Returns:
            string: IP address in decimal dot notation
        """
        # Pad IP's prefix with 1's until string length is 8 in a list
        # Then add 3 lists each with 8 1's in them. Convert to decimal dot.
        return to_decimal_dot([self.prefix.ljust(8, "1")] + (["1" * 8] * 3))


    def to_cidr_notation(self):
        """
        Determines CIDR notation of a subnet.

        Returns:
            string: IP address in CIDR notation
        """
        bin_subnet_string = "".join(to_binary_string(self.subnet_mask))

        # Uses i as a counter until first 0 is found in binary IP address
        for i in range(len(bin_subnet_string)):
            if bin_subnet_string[i] == "0":
                return self.ip_dot_str + f"/{str(i)}"


    def how_many_subnets(self):
        """
        Determines number of subnets based on class, CIDR and subnet mask.

        Returns:
            int: number of subnets
        """
        bin_subnet = to_binary_string(self.subnet_mask)
        # Calculate based on number of host bits in last byte if class is C
        # or if class ic B and cidr is greater than 23
        if self.ip_class == "C" or ((self.ip_class == "B" or self.ip_class == "A") and int(self.cidr_notation.split("/")[-1]) > 23):
            return 2**(bin_subnet[-1].count("1"))

        # Calculate based on number of host bits in third byte if class is B
        # and cidr is less than 24 or class is A and cidr is greater than 15
        elif self.ip_class == "B" or (self.ip_class == "A" and int(self.cidr_notation.split("/")[-1]) > 15):
            return 2**((bin_subnet[2]).count("1"))

        # Calculate based on number of host bits in second byte if class is A
        # and cidr is less than 16
        elif self.ip_class == "A":
            return 2**((bin_subnet[1]).count("1"))


    def how_many_addressable_hosts(self):
        """
        Determines number of addressable hosts based on subnet mask.

        Returns:
            int: number of addressable hosts
        """
        bin_subnet_string = "".join(to_binary_string(self.subnet_mask))
        # 2 to power of Number of unmasked bits minus 2 for host and
        # broadcast addresses
        return (2**(bin_subnet_string.count("0"))) - 2


    def what_valid_subnets(self):
        """
        Determines valid subnets based on IP address, class, CIDR and subnet mask.

        Returns:
            list: list of valid subnets
        """
        subnets = []
        counter = 0

        # Calculate based on last byte if class is C or if class ic B and cidr
        # is greater than 23
        if self.ip_class == "C" or ((self.ip_class == "B" or self.ip_class == "A") and int(self.cidr_notation.split("/")[-1]) > 23):
            block_size = 256 - int(self.subnet_mask.split(".")[-1])
            limit = int(self.subnet_mask.split(".")[-1])
            while counter <= limit:
                subnets.append(".".join(self.ip_dot_str.split(".")[:-1]) + f".{str(counter)}")
                counter += block_size
        # Calculate based on last byte if class is B and cidr is less than 24
        elif self.ip_class == "B" or (self.ip_class == "A" and int(self.cidr_notation.split("/")[-1]) > 15):
            block_size = 256 - int(self.subnet_mask.split(".")[2])
            limit = int(self.subnet_mask.split(".")[2])
            while counter <= limit:
                subnets.append(".".join(self.ip_dot_str.split(".")[:2]) + f".{str(counter)}.0")
                counter += block_size
        elif self.ip_class == "A":
            block_size = 256 - int(self.subnet_mask.split(".")[1])
            limit = int(self.subnet_mask.split(".")[1])
            while counter <= limit:
                subnets.append(".".join(self.ip_dot_str.split(".")[:1]) + f".{str(counter)}.0.0")
                counter += block_size
        return subnets


    def what_broadcast_addresses(self):
        """
        Determines broadcast addresses based on IP address, class, CIDR and subnets.

        Returns:
            list: list of broadcast addresses
        """
        broadcasts = []
        # Calculate based on last byte if class is C or if class ic B and cidr
        # is greater than 23
        if self.ip_class == "C" or ((self.ip_class == "B" or self.ip_class == "A") and int(self.cidr_notation.split("/")[-1]) > 23):
            for s in self.valid_subnets[1:]:
                last_byte = int(s.split(".")[-1])
                broadcasts.append(".".join(self.ip_dot_str.split(".")[:-1]) + f".{str(last_byte - 1)}")
            broadcasts.append(".".join(self.ip_dot_str.split(".")[:-1]) + ".255")
        # Calculate based on last byte if class is B and cidr is less than 24
        elif self.ip_class == "B" or (self.ip_class == "A" and int(self.cidr_notation.split("/")[-1]) > 15):
            for s in self.valid_subnets[1:]:
                third_byte = int(s.split(".")[2])
                broadcasts.append(".".join(self.ip_dot_str.split(".")[:2]) + f".{str(third_byte - 1)}.255")
            broadcasts.append(".".join(self.ip_dot_str.split(".")[:2]) + ".255.255")
        elif self.ip_class == "A":
            for s in self.valid_subnets[1:]:
                second_byte = int(s.split(".")[1])
                broadcasts.append(".".join(self.ip_dot_str.split(".")[:1]) + f".{str(second_byte - 1)}.255.255")
            broadcasts.append(".".join(self.ip_dot_str.split(".")[:1]) + "255.255.255")
        return broadcasts


    def what_subnet_firsts(self):
        """
        Determines first addresses based on IP address, class, CIDR and subnets.

        Returns:
            list: list of first addresses
        """
        firsts = []
        # Calculate based on last byte if class is C or if class ic B and cidr
        # is greater than 23
        if self.ip_class == "C" or ((self.ip_class == "B" or self.ip_class == "A") and int(self.cidr_notation.split("/")[-1]) > 23):
            for s in self.valid_subnets:
                last_byte = int(s.split(".")[-1])
                firsts.append(".".join(self.ip_dot_str.split(".")[:-1]) + f".{str(last_byte + 1)}")
        # Calculate based on last byte if class is B and cidr is less than 24
        elif self.ip_class == "B" or (self.ip_class == "A" and int(self.cidr_notation.split("/")[-1]) > 15):
            for s in self.valid_subnets:
                third_byte = int(s.split(".")[2])
                firsts.append(".".join(self.ip_dot_str.split(".")[:2]) + f".{str(third_byte)}.1")
        elif self.ip_class == "A":
            for s in self.valid_subnets:
                second_byte = int(s.split(".")[1])
                firsts.append(".".join(self.ip_dot_str.split(".")[:1]) + f".{str(second_byte)}.0.1")
        return firsts


    def what_subnet_lasts(self):
        """
        Determines last addresses based on IP address, class, CIDR and subnets.

        Returns:
            list: list of last addresses
        """
        lasts = []
        # Calculate based on last byte if class is C or if class ic B and cidr
        # is greater than 23
        if self.ip_class == "C" or ((self.ip_class == "B" or self.ip_class == "A") and int(self.cidr_notation.split("/")[-1]) > 23):
            for s in self.broadcast_addresses:
                last_byte = int(s.split(".")[-1])
                lasts.append(".".join(self.ip_dot_str.split(".")[:-1]) + f".{str(last_byte - 1)}")
        # Calculate based on last byte if class is B and cidr is less than 24
        elif self.ip_class == "B" or (self.ip_class == "A" and int(self.cidr_notation.split("/")[-1]) > 15):
            for s in self.broadcast_addresses:
                third_byte = int(s.split(".")[2])
                lasts.append(".".join(self.ip_dot_str.split(".")[:2]) + f".{str(third_byte)}.254")
        elif self.ip_class == "A":
            for s in self.broadcast_addresses:
                second_byte = int(s.split(".")[1])
                lasts.append(".".join(self.ip_dot_str.split(".")[:1]) + f".{str(second_byte)}.255.254")
        return lasts


class Supernet:
    def __init__(self, ip_addr_list):
        """
        Initialises required attributes of an Supernet object.

        Args:
            ip_addr_list (list): A list of IP addresses in decimal dot notation
        """
        self.ip_addr_list = [IPAddress(x) for x in ip_addr_list]
        self.supernet_cidr_notation = self.what_supernet_cidr_notation()[0]
        self.prefix_length = self.what_supernet_cidr_notation()[1]
        self.network_mask = self.what_network_mask()


    def __str__(self):
        """
        Compiles a message of the stats of the Supernet object.
        """
        message = ""
        message += f"Address: {self.supernet_cidr_notation}\n"
        message += f"Network Mask: {self.network_mask}"
        return message


    def what_supernet_cidr_notation(self):
        """
        Determines the CIDR notation of the supernet.

        Returns:
            list:
                string: first IP address of supernet in CIDR notation
                int: length of common prefix of supernet addresses
        """
        bin_ip_addr_list = ["".join(to_binary_string(x.ip_dot_str)) for x in self.ip_addr_list]
        prefix_length = len(commonprefix(bin_ip_addr_list))
        return [self.ip_addr_list[0].ip_dot_str + f"/{prefix_length}", prefix_length]


    def what_network_mask(self):
        """
        Determines the network mask of the supernet.

        Returns:
            string: network mask for supernet
        """
        bin_mask = ("1" * self.prefix_length) + ("0" * (32 - self.prefix_length))
        return to_decimal_dot([bin_mask[i:i + 8] for i in range(0, len(bin_mask), 8)])


#  Scriney's helper functions

def to_binary_string(ip_addr):
    """
    Converts an ip address represented as a string in decimal dot notation into
    a list of four binary strings each representing one byte of the address.

    :param ip_addr: The ip address as a string in decimal dot notation
    e.g. "132.206.19.7" + self.ip_dot_str.split(".")[ based on whether there is
        a subnet mask.-1]

    :return: An array of four binary strings each representing one byte
    of ip_addr e.g.
    ['10000100', '11001110', '00010011', '00000111']
    """
    byte_split = ip_addr.split(".")
    return ['{0:08b}'.format(int(x)) for x in byte_split]


def to_decimal_dot(ip_addr_list):
    """
    Take in an array of four strings represting the bytes of an ip address
    and convert it back into decimal dot notation

    :param ip_addr_list: An array of four binary strings each
    representing one byte of ip_addr e.g. ['10000100', '11001110',
    '00010011', '00000111']

    :return: The ip address as a string in decimal dot notation e.g.
    '132.206.19.7'
    """
    return ".".join([str(int(x,2)) for x in ip_addr_list])
