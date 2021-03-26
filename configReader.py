import re

def config(filename):

    config_info = {}
    file = open(filename, "r")
    file_lines = []

    for line in file.readlines():
        line = re.split(', | |\n', line)
        file_lines.append(line)

    router_id = int(file_lines[0][1])
    input_ports = file_lines[1][1:7]
    output_ports = file_lines[2][1:4]

    outputs = output_func(output_ports)

    config_info[router_id] = outputs


    return config_info

def output_func(output_ports):
    fowarding_table = {}
    for outputs in output_ports:
        output = re.split('-', outputs)
        neighbour = int(output[2])
        cost = int(output[1])
        port_number = int(output[0])
        fowarding_table[neighbour] = [cost, port_number]

    return fowarding_table


print(config("router1.txt"))