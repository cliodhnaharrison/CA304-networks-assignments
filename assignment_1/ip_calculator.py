#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from networking import IPAddress, Supernet


def get_class_stats(ip_addr):
    """
    Prints out stats for given IP address.

    Args:
        ip_addr (str): IPv4 address in decimal dot notation e.g. ("136.206.18.7")
    """
    print(IPAddress(ip_addr))


def get_subnet_stats(ip_addr, subnet_mask):
    """
    Prints out stats for given subnet.

    Args:
        ip_addr (str): IPv4 address in decimal dot notation
        subnet_mask (str): string subnet mask for ip_addr
    """
    print(IPAddress(ip_addr, subnet_mask))


def get_supernet_stats(ip_addr_list):
    """
    Prints out stats for given supernet.

    Args:
        ip_addr_list (list): list of contigous class C addresses
    """
    print(Supernet(ip_addr_list))
