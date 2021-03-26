import re

def config(filename):

    routing_table = {}
    file = open(filename, "r")
    file_lines = []

    for line in file.readlines():
        line = re.split(', | |\n', line)
        file_lines.append(line)

    router_id = file_lines[0][1]
    input_ports = file_lines[1][1:7]
    output_ports = file_lines[2][1:4]

    for outputs in output_ports:
        output = re.split('-', outputs)
        neighbour = output[2]
        cost = int(output[1])
        port_number = int(output[0])
        routing_table[neighbour] = [cost, port_number]


    print(router_id, input_ports ,routing_table)

    return "hello"

print(config("router1.txt"))