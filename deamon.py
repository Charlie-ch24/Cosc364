"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter (27380476)
Router main program
"""
########## Header ##########
import deamon_sup as system
import socket, select
import sys, time, random # must use
import traceback # optional features
from router import *
from timer import *

LocalHost = "127.0.0.1"
ROUTER = None # Router Obj
SOCKETS = [] # Enabled Interfaces

########## Body ##########
def createSocket():
    for port in ROUTER.INPUT_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LocalHost, port))
        SOCKETS.append(sock)

def send():
    """ Send forwarding table to neighbour routers """
    for destID, link in ROUTER.OUTPUT_PORTS.items():
        table = ROUTER.get_routing_table(destID)
        message = system.create_rip_packet(table)
        dest = (LocalHost, link[0])
        for sock in SOCKETS:
            if sock.getsockname()[1] % 10 == destID:
                sock.sendto(message, dest)
                break

def send_periodic():
    """ Execute periodically """
    if not ROUTER.is_expired(RTimer.PERIODIC_TIMEOUT, time.time()):
        return

    send()
    ROUTER.reset_timer(RTimer.PERIODIC_TIMEOUT) # Reset timer after sent to all neighbour
    print(f"Routing Table (periodic) sent to neighbours at {time.strftime('%X')}.\n")

def send_expired_entry():
    """ Check and send if at least 1 entry expired """
    if not ROUTER.has_expired_entry():
        return

    send()
    ROUTER.reset_timer(RTimer.PERIODIC_TIMEOUT) # Reset timer
    print(f"Routing Table (expiry) sent to neighbours at {time.strftime('%X')}.\n")

def garbage_collection():
    ROUTER.garbage_collection()

def receive(timeout = 1):
    """ Return True if some data received """
    readable, _, _ = select.select(SOCKETS, [], [], timeout)
    for sock in readable:
        data, sender = sock.recvfrom(1024)
        if not ROUTER.is_expected_sender(sender):
            print(f"Droped message on {sender} -> {sock.getsockname()} link!")
            continue
        routes = system.process_rip_packet(data)
        ROUTER.update_route_table(routes, time.time())

########## Program ##########
def init_router():
    global ROUTER # include this if modifying global variable
    filename = sys.argv[1]
    rID, inputs, outputs, timeout = system.read_config(filename)

    #  Router instance with default routing table
    timestamp = time.time()
    ROUTER = Router(rID, inputs, outputs, timestamp, timeout)
    ROUTER.print_hello()

    # First time notice to neighbours
    createSocket()
    ROUTER.print_route_table(timestamp, time.strftime('%X'))
    send_periodic()

if __name__ == "__main__":
    try:
        init_router()
        while True:
            print("Waiting for incoming message ...")
            receive()
            ROUTER.print_route_table(time.time(), time.strftime('%X'))
            send_expired_entry()
            send_periodic()
            garbage_collection()

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