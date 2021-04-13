"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""
########## Header ##########
import deamon_sup as system
import socket, select
import sys, time, random # must use
import traceback # optional features
from router import *

LocalHost = "127.0.0.1"
ROUTER = None # Router Obj
SOCKETS = [] # Enabled Interfaces

########## Body ##########
def createSocket():
    for port in ROUTER.INPUT_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LocalHost, port))
        SOCKETS.append(sock)

def send(state):
    """ Send forwarding table to neighbour routers """
    packets = []
    head = system.create_head(ROUTER.ROUTER_ID)
    for out in ROUTER.OUTPUT_PORTS.items():
        rip_entry = system.create_rip_entry(out[1][0], out[1][1])
        packet = head + rip_entry
        packets.append(packet)
    for pack in packets:
        if system.packet_check(pack):
            print("good")
        else:
            print("uhoh")





    for sock in SOCKETS:
        pass

    status = "No-change"
    if state is None:
        status = "Default"
    elif state is True:
        status = "Updated"
    print("Routing Table ({0}) sent to neighbours.".format(status))

def receive(timeout = 3):
    """ return True if some data received """
    readable, _, _ = select.select(SOCKETS, [], [], timeout)
    for sock in readable:
        data, _ = sock.recvfrom(1024) # sender not needed
        routes = system.process_Rip_adv(data)
        ROUTER.update_route_table(routes)
    # return True if len(readable) > 0 else False
    routes = []
    return ROUTER.update_route_table(routes)

########## Program ##########
def init_router():
    global ROUTER # include this if modifying global variable
    filename = sys.argv[1]
    rID, inputs, outputs = system.read_config(filename)

    # Create Router instance with default routing table
    ROUTER = Router(rID, inputs, outputs)
    ROUTER.print_hello()

    # First time notice to neighbours
    createSocket()
    ROUTER.print_route_table()
    send(None) # periodic every 30 sec
    
if __name__ == "__main__":
    try:
        init_router()
        while True:
            is_updated = receive()
            ROUTER.print_route_table()
            send(is_updated)
    except IndexError:
        print("Error: Config file is not provided!")
    except FileNotFoundError:
        print("Error: given Config file not found!")
    except ValueError as v_err:
        print("Warning:", v_err)
    except socket.error as s_err:
        print("Error:", s_err)
    except KeyboardInterrupt:
        print("\n******** Deamon exit successfully! Router shuting down... ********")
    except Exception as e:
        traceback.print_exc() # Traceback unknown error
        print("Program exited unexpectedly.\n")
    finally:
        print()
        sys.exit()
