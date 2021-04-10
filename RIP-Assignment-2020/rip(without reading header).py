import sys
import socket
import os
import select
import time
import random
import pickle
import copy

#global variables
HOST = '127.0.0.1'
INFINITY = 16

# router id : [cost, recieved_from, timer]
forwarding_table = {}
outputs = []
inputs = []
socks = []
neighbors = []
ROUTERS = []

def check_router_id(routerId):
        """Check if routerId is in valid range"""
        if int(routerId) >= 1 and int(routerId) <= 64000:
                return routerId
        else:
                print('Invalid router Id')

def check_port(ports):
        """Check if port# is in valid range"""
        validPorts = []
        for p in ports:
                if int(p) >= 1024 and int(p) <= 64000:
                        validPorts.append(int(p))           
        return validPorts

def check_output(outputs, validPorts):
        """Check if outputs are valid"""
        outputs_dict = {}
        for output in outputs:
                port, metric, destID = output.split('-') 
                port, metric, destID = int(port), int(metric), int(destID)
                
                #check if the port does not in range
                if int(port) < 1024 or int(port) > 64000:
                        print('PortNum is out of range')
                        sys.exit()
                #check if any ports of neighbors in this router
                if port in validPorts:
                        print('PortNum could not appear in neighbor(s)')
                        sys.exit()
                outputs_dict[port] = [metric, destID]
                neighbors.append(destID)
                
        return outputs_dict

def read_config(filename):
        global router_id
        
        configFile = open(filename)
        readFile = configFile.readlines()
        flag = 0
        checkRouter = 0
        checkPort = 0
        checkOutput = 0
        for line in readFile:
                if line.startswith("router-id"):
                        checkRouter = 1
                        _, router_id = line.split()
                        router_id = int(check_router_id(router_id))
                        if router_id in ROUTERS:
                                print('router Id should be unique')
                        else:
                                ROUTERS.append(router_id)
                        
                elif line.startswith("input-ports"):
                        checkPort = 1
                        ports = line.split()
                        ports = [i.strip(',') for i in ports[1:]]
                        # check if port unique in list 
                        flag = len(set(ports)) == len(ports)
                        if (flag):
                                pass
                        else:
                                print('Port must be unique')
                        
                elif line.startswith("outputs"):
                        checkOutput = 1
                        outputs = line.split()
                        outputs = [i.strip(',') for i in outputs[1:]]
          
        if (checkRouter and checkPort and checkOutput) == 0:
                print("Config file is incomplete")
                # quit
                sys.exit()
        else:
                input_ports = check_port(ports)
                checked_outputs_dict = check_output(outputs, ports)
        
        return router_id, input_ports, checked_outputs_dict

        
def create_socket(ports):
        """Returns a binded socket"""
        sockets = []
        try: 
                for i in ports:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.bind(("", i))
                        sockets.append(s)
                return sockets
        except socket.error: 
                print("failed to create socket")
            
            
def create_packet(forwarding_table):
        """encode the packet to send to another routers"""
        pack = {}
        pack['version'] = 2
        pack['router_id'] = router_id
        pack['data'] = forwarding_table
        data = pickle.dumps(pack)
        return data

# pkt = [ver, router_id, data = {destID: cost, timer, reachable}]
 
# forwarding table = {destID : [metric, timer, reachable]}

def send_packet(port):
        """send packet by all input ports"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = create_packet(forwarding_table)
        s.sendto(data, (HOST, port))
        
def receive_packet(socks, original, timeout=1):
        """receive forwarding table of another routers in network"""
        org = copy.deepcopy(original)
        readable, _, _ = select.select(socks, [], [], timeout)
        for s in readable:
                data, addr = s.recvfrom(1024)
                pkt = pickle.loads(data)
                neighbor = pkt['router_id']
                #forwarding_table is too long so i defined it as table temply
                table = forwarding_table
                for key, values in pkt['data'].items():
                        cost, timer, reachable = values
                        # if values in the packet are not in the forwarding table (non-neighbors) , add-up
                        if key not in table:
                                best_cost = min(cost + table[neighbor][0], INFINITY)
                                table[key] = [best_cost, 0, 'non-neighbor']
                
                
                
def update_forwarding_table_with_timer(forwarding_table):
        
        return 0
        #invalidTimer = 0  # timer
        #invalidTimer += (now - then)
        #forwarding_table[router][1] += (now - then)
        #print(invalidTimer, 'this is the timer')
        #forwarding_table[router][reachable] += (elapsed - then)
        #print(forwarding_table.keys(), 'this is the new one')
                #garbage_timer = 0
                #if invalidTimer >= 10:
                        #forwarding_table[router][reachable] = 'maybe die'
                #if invalidTimer >= 15:
                        #forwarding_table[router][cost] = INFINITY
                        #garbage_timer += 15
                #if garbage_timer >= 5:
                        #garbages.append(router)

#for i in garbages:
        #if i in forwarding_table.keys():
                #forwarding_table.pop(i)
        
                
def update_forwarding_table(read_pkt):
        """update the forwarding table ( will divide the code above to here but only when finish everything )"""    
        return 0

def print_forwarding_table():
        lines = "---------------------------------------------------------------"
        print(lines)
        print("FORWARDING TABLE OF ROUTER ID " + str(router_id))
        print("  {:^9} || {:^9} || {:^9} || {:^9} ".format("Router", "Metric", "Timer", "Reachable"))
        for router, info in forwarding_table.items():
                if router != router_id:
                        cost, timer, reachable = info
                        print("  {:^9} || {:^9} || {:^9.1f} || {:^9} ".format(router , cost, timer, reachable))
                #print("Router ID:", router, "Metric:", cost, "Learnt from:", learnt_from, "Timer:", timer)
        print(lines)
        print('\n')

        
def main():        
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
        
        # {router ID : [metric, timer reachable]}
        
        # set up the default forwarding table with only neighbors connecting to
        for vals in outputs.values():
                dest = vals[1]
                metric = vals[0]
                forwarding_table[dest] = [metric, 0, 'True']
        
        print(forwarding_table, 'this is forwarding table with update')
        original = copy.deepcopy(forwarding_table)
        socks = create_socket(input_ports)
        print(socks)
        
        while True:
                garbages = []
                garbage_timer = 0
                then = time.time()
                for router in original.keys():
                        if router_id != router:
                                now = time.time()                
                                forwarding_table[router][1] += (now - then)
                                if forwarding_table[router][2] != 'True' or forwarding_table[router][2] != 'non-neighbor':
                                        garbage_timer += (now-then)
                                if forwarding_table[router][2] == 'True':
                                        forwarding_table[router][1] = 0.0
                                if garbage_timer > 15:
                                        garbages.append(router)
                print(garbage_timer)
                receive_packet(socks, original)
                
                
                #update_forwarding_table(pkts)
                #update_forwarding_table_with_timer(forwarding_table)
                
                print_forwarding_table()                
                
                for port in outputs.keys():
                        send_packet(int(port))
                
                time.sleep(1)
                continue
main()
    

