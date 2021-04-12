"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router support function
"""
import os, sys
import numpy as np

FILE_EXTENSION = ".txt"

def create_head(rID):
    command = 1
    verison = 2
    rID = 0
    command = command.to_bytes(1, byteorder='big')
    verison = verison.to_bytes(1, byteorder='big')
    rID = rID.to_bytes(2, byteorder='big')
    header = bytearray(command + verison + header_zero)
    print(header, "Header")
    return header

def create_rip_entry(destID, metric):
    address_fam_id = 0
    zero = 0
    address_fam_id = address_fam_id.to_bytes(2, byteorder='big')
    zero_2b = zero.to_bytes(2, byteorder='big')
    dest_ID = destID.to_bytes(4, byteorder='big')
    zero_8b = zero.to_bytes(8, byteorder='big')
    metric = metric.to_bytes(4, byteorder='big')

    rip_entry = bytearray(address_fam_id + zero_2b + dest_ID + zero_8b + metric)
    return rip_entry


def create_packet(rID, destID, metric):
    #request command = 1 but response command = 2
    header = create_head(rID)
    rip_entry = create_rip_entry(destID, metric)

    return header + rip_entry

    # Rip entry 20 bytes





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