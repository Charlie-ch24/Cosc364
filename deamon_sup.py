"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router support function
"""
import os, sys
import numpy as np
from router import *

FILE_EXTENSION = ".txt"

def create_head(rID):
    "Creates the 4 byte header"
    command = 1
    verison = 2
    command = command.to_bytes(1, byteorder='big')
    verison = verison.to_bytes(1, byteorder='big')
    rID = rID.to_bytes(2, byteorder='big')
    header = bytearray(command + verison + rID)
    return header

def create_rip_entry(destID, metric):
    "Creates the 20 byte body of packet"
    address_fam_id = 0
    zero = 0
    address_fam_id = address_fam_id.to_bytes(2, byteorder='big')
    zero_2b = zero.to_bytes(2, byteorder='big')
    dest_ID = destID.to_bytes(4, byteorder='big')
    zero_8b = zero.to_bytes(8, byteorder='big')
    metric = metric.to_bytes(4, byteorder='big')

    rip_entry = bytearray(address_fam_id + zero_2b + dest_ID + zero_8b + metric)
    return rip_entry


def packet_check(packet):
    "Makes sure packet doesnt have errors when converted"
    metric = int.from_bytes(packet[20:24], byteorder='big')
    dest_id = int.from_bytes(packet[8:12], byteorder='big')
    r_id = int.from_bytes(packet[2:4], byteorder='big')
    version = int.from_bytes(packet[1:2], byteorder='big')
    command = int.from_bytes(packet[0:1], byteorder='big')
    print(dest_id, metric, r_id, version, command, "ipv4", "cost", "r_id", "verison", "command")
    if is_valid_ports(dest_id) and (0 < r_id or r_id > 64000) and (version == 2):
        return True
    return False












def read_config(filename):
    rID, inputs, outputs = None, None, None
    if filename.endswith(FILE_EXTENSION):
        config_file = open(filename)
    else:
        config_file = open(filename + FILE_EXTENSION)
    config_data = config_file.readlines()

    for line in config_data:
        head, data = line.split(':')
        if head == "router-id":
            rID = int(data)
            if not 0 < rID or rID > 64000:
                raise ValueError("Router ID must be between 1 and 64000.")
        elif head == "input-ports":
            inputs = [int(port) for port in data.rstrip().split(',')]
            if not is_valid_ports(inputs):
                raise ValueError("Invalid input port(s) in config data.\nPorts must be between 1024 and 64000.")
        elif head == "outputs":
            outputs = [port.strip() for port in data.rstrip().split(',')]            
            ports = [int(output.split('-')[0]) for output in outputs]
            if not is_valid_ports(ports):
                raise ValueError("Invalid output port(s) in config data.\nPorts must be between 1024 and 64000.")

    return rID, inputs, outputs

def is_valid_ports(ports):
    ports = np.array(ports)
    return np.all((ports >= 1024) & (ports <= 64000))

def create_Rip_adv():
    pass

def process_Rip_adv(packet):
    return []