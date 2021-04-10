"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router support function
"""
import os, sys

FILE_EXTENSION = ".txt"

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
        elif head == "input-ports":
            inputs = [int(port) for port in data.rstrip().split(',')]
        elif head == "outputs":
            outputs = [port.strip() for port in data.rstrip().split(',')]
            
    return rID, inputs, outputs
