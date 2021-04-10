# Christina Shepherd
# 39033676
# Linh Khanh LUU
# 68697438

import sys
import socket
import os
import select
import time
import random

#global variables
HOST = '127.0.0.1'
ROUTERS = []
PORTS = []
OUTPUTS = {}
SOCKETS = []
INFINITY = 16

# default timer values
TIMER = 30
TIMEOUT = (180)
GARBAGE = (120) + TIMEOUT 

# router id : [cost, recieved_from, timer, reachable]
FORWARDING_TABLE = {}

def check_router_id(routerId):
        """Check if routerId is in valid range"""
        if int(routerId) >= 1 and int(routerId) <= 64000:
                return routerId
        else:
                print('Invalid router ID')
                sys.exit()

def check_port(ports):
        """Check if port# is in valid range"""
        validPorts = []
        for p in ports:
                if int(p) >= 1024 and int(p) <= 64000:
                        validPorts.append(int(p))
                else:
                        print("Invalid input port number")
                        sys.exit()
        return validPorts

def check_output(outputs, validPorts):
        """Check if outputs are valid"""
        outputs_dict = {}
        for output in outputs:
                port, metric, routerId = output.split('-') 
                port, metric, routerId = int(port), int(metric), int(routerId)

                # check if the port does not in range
                if int(port) < 1024 or int(port) > 64000:
                        print('Port number is out of range')
                        sys.exit()
                
                # check if any ports of neighbors in this router
                if port in validPorts:
                        print('Port number could not appear in neighbor(s)')
                        sys.exit()
                outputs_dict[port] = [metric, routerId]
                        
        return outputs_dict

def read_config(filename):
        """ Reads the config file and returns all necessary infomation to implement a forwarding table """
        global router_id
        global TIMER
        global TIMEOUT
        global GARBAGE
        
        # open and read the config file
        configFile = open(filename)
        readFile = configFile.readlines()
        
        # set up some checking flags
        flag = 0
        checkRouter = 0
        checkPort = 0
        checkOutput = 0
        for line in readFile:
                if line.startswith("router-id"):
                        # set 1 if router-id in the config file
                        checkRouter = 1
                        _, router_id = line.split()
                        router_id = int(check_router_id(router_id))
                        if router_id in ROUTERS:
                                print('router Id should be unique')
                        else:
                                ROUTERS.append(router_id)
                        
                elif line.startswith("input-ports"):
                        # set 1 if input-ports section in the config file
                        checkPort = 1
                        ports = line.split()
                        ports = [i.strip(',') for i in ports[1:]]
                        # check if port unique in list 
                        flag = len(set(ports)) == len(ports)
                        if (flag):
                                pass
                        else:
                                print('Port must be unique')
                                sys.exit()
                        
                elif line.startswith("outputs"):
                        # set 1 if outputs section in the config file
                        checkOutput = 1
                        outputs = line.split()
                        outputs = [c.strip(',') for c in outputs[1:]]
                        
                elif line.startswith("timer"):
                        line = line.split()
                        TIMER = int(line[1])
                        TIMEOUT = TIMER * 6
                        GARBAGE = TIMER * 10
                        
                        
        # check if the configuration file included all 3 required parts
        # router_id, input_ports and outputs               
        if (checkRouter and checkPort and checkOutput) == 0:
                print("Config file is incomplete")
                sys.exit()
        else:
                # check the inputs and outputs of the router
                input_ports = check_port(ports)
                outputs = check_output(outputs, input_ports)
        
        return router_id, input_ports, outputs

        
def create_socket(port):
        """Returns a binded socket"""
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind((HOST, port))
                return s
        except socket.error:
                print("Error occurred. Unable to create socket")
                sys.exit()
        
def response(socks, timeout=1):
        """Responses a message from UDP Server"""
        readable, _, _ = select.select(socks, [], [], timeout)
        for socket in readable:
                data, addr = socket.recvfrom(1024)
                read_packet(data)    

def create_payload(addr_fam_id, ipv4, router, metric):
        """ Create a single RIP entry """
        # address family id (2 bytes)
        addr_fam_id1 = (addr_fam_id >> 8) & 0xff
        addr_fam_id2 = addr_fam_id & 0xff

        #router_id (2 bytes)
        router_id1 = (router >> 8) & 0xff
        router_id2 = router & 0xff        
        
        #ipv4 (4 bytes)
        ipv4_1 = (ipv4 >> 24) & 0xff
        ipv4_2 = (ipv4 >> 16) & 0xff
        ipv4_3 = (ipv4 >> 8) & 0xff
        ipv4_4 = ipv4 & 0xff

        #metric (4 bytes)
        metric1 = (metric >> 24) & 0xff
        metric2 = (metric >> 16) & 0xff
        metric3 = (metric >> 8) & 0xff
        metric4 = metric & 0xff   
        
        # 20 bytes
        return bytearray([addr_fam_id1, addr_fam_id2, router_id1, router_id2, ipv4_1, ipv4_2, ipv4_3, ipv4_4, 0, 0, 0, 0, 0, 0, 0, 0, metric1, metric2, metric3, metric4])

def create_packet(command, version, full_payload, router):
        """ Attach the header and all the RIP entries """
        command = command & 0xff
        version = version & 0xff
        
        # generating router ID
        router_id1 = (router >> 8) & 0xff
        router_id2 = router & 0xff          
        
        return bytearray([command, version, router_id1, router_id2]) + bytearray(full_payload)

def read_packet(message):
        """ Read a recieved packet and extract information """
        command = message[0]
        version = message[1]
        
        # learnt from router
        generated_router = message[2]<<8 | message[3]
        length_entries = len(message)
        i = 4
        while i < length_entries:
                router_id = message[i+2]<<8 | message[i+3]
                metric = message[i+16]<<24 | message[i+17]<<16 | message[i+18]<<8 | message[i+19]
                add_to_forwarding_table(router_id, generated_router, metric)
                i += 20

def create_message(output_port, output_cost, output_router, router_id):
        # Message info from RIPv2 specification:
        # command = 1 is request, 2 is response (1 byte)
        # version = 2 (always 2) (1 byte)
        # unused = 0 (2 bytes) - use for generating router
        # rip entry: (20 bytes) (payload)
        # can be 1 - 25 entries
        # address family id (2 bytes)
        # unused = 0 (2 bytes) - use this for router id
        # IPv4 adress (4 bytes) - we dont care about this
        # unused = 0 (4 bytes) 
        # unused = 0 (4 bytes)
        # metric (4 bytes) 
        
        #header:
        command = 2
        version = 2
        full_payload = bytearray()
        
        # RIP entries:
        # create payload for each entry in forwarding table
        for router, info in FORWARDING_TABLE.items():
                cost, recieved_from, timer, _ = info
                # prevent loops
                if recieved_from == output_router:
                        cost = INFINITY
                # add cost to neighbour router this will be sent to        
                else:
                        cost = min(cost + output_cost, INFINITY)
                payload = create_payload(0, 0, router, cost)
                full_payload += payload
                
        packet = create_packet(command, version, full_payload, router_id)
        return packet

        
def send_data(outputs):
        """ To send the packet to the other routers according to the port num """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for port, value in outputs.items():
                cost, out_router = value        
                message = create_message(port, cost, out_router, router_id)
                s.sendto(message, (HOST, port)) 

def add_to_forwarding_table(router, learnt_from_router, new_metric):
        """ Adds routers to forwarding table that was learnt from neighbours """
        # check if the entry is already in the forwarding table
        if router in FORWARDING_TABLE:
                cost, learnt, _, _ = FORWARDING_TABLE[router]
                # if the metric is valid
                if new_metric < INFINITY:
                        # if same info already exists, reset timer
                        if new_metric == cost and learnt == learnt_from_router:
                                FORWARDING_TABLE[router] = [new_metric, learnt_from_router, 0.0, 'True']
                        # the older path is faster
                        if new_metric < cost:
                                FORWARDING_TABLE[router] = [new_metric, learnt_from_router, 0.0, 'True']
                                print_forwarding_table()
                
                # if the metric is invalid (reaches 16)
                else:
                        # detects where the invalid router in the forwarding_table
                        if learnt == learnt_from_router:
                                # set the metric to infinity for further step in the
                                # update function
                                FORWARDING_TABLE[router][0] = INFINITY
                                FORWARDING_TABLE[router][3] = 'False'
                                
        # if not in table then add it if cost is valid
        else:
                if new_metric < INFINITY:
                        FORWARDING_TABLE[router] = [new_metric, learnt_from_router, 0, 'True']
                        print_forwarding_table()

def update_forwarding_table():
        """ Keeps track on timer everytime there is a change in the forwarding table """
        garbages = []
        # set timer
        then = time.time()
        
        # random timer +/- 20%
        time.sleep(random.uniform(TIMER*0.8, TIMER*1.2))
        original = FORWARDING_TABLE.copy()
        
        for router in original.keys():
                if router != router_id:
                        elapsed = time.time()
                        
                        # increase timer value
                        FORWARDING_TABLE[router][2] += (elapsed - then)
                        
                        # garbage collection
                        if FORWARDING_TABLE[router][2] >= GARBAGE:
                                garbages.append(router)
                        
                        # Timeout                      
                        elif FORWARDING_TABLE[router][2] >= TIMEOUT:
                                FORWARDING_TABLE[router][3] = 'False'
                                FORWARDING_TABLE[router][0] = INFINITY
                        
                        # if the metric is set to 16 then removes it from the forwarding table
                        #when the timer reaches the garbage-collection timer (for non-neighbors)
                        elif FORWARDING_TABLE[router][0] == INFINITY:
                                if FORWARDING_TABLE[router][2] >= (GARBAGE - TIMEOUT):
                                        garbages.append(router)                        
                           
        for key in garbages:
                FORWARDING_TABLE.pop(key)               

def print_forwarding_table():
        """ Prints the forwarding table """
        lines = "-----------------------------------------------------------------"
        print(lines)
        print("FORWARDING TABLE OF ROUTER_ID = " + str(router_id))
        print("  {:^9} || {:^9} ||  {:^9} || {:^9} || {:^9} ".format("Router", "Next-hop", "Metric", "Timer", "Reachable"))
        for router, info in sorted(FORWARDING_TABLE.items()):
                if router != router_id:
                        cost, learnt_from, timer, reachable = info
                        print("  {:^9} ||  {:^9} ||  {:^9} || {:^9.1f} || {:^9} ".format(router, learnt_from, cost, timer, reachable))
        print(lines)
        print('\n')
        
def main(): 
        """ Main function to run the program """
        try:
                filename = sys.argv[1]
        except IndexError:
                print("Error: not filename given")
                sys.exit()

        if os.path.exists(filename):
                router_id, input_ports, outputs = read_config(filename)
        else:
                print("Error: file does not exist")
                sys.exit()
                
        FORWARDING_TABLE[router_id] = [0, router_id, 0, 'None']
        
        for port in input_ports:
                PORTS.append(port)
                sock = create_socket(port)
                SOCKETS.append(sock)
        
        for key, value in outputs.items():
                OUTPUTS[key] = value

        while True:
                update_forwarding_table()
                send_data(OUTPUTS)
                response(SOCKETS)
                print_forwarding_table()              
                
                continue
                
main()