"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter (27380476)
Router main program
"""
########## Header ##########
from daemon_sup import *
import socket, time, select
import sys, random # must use
import traceback # optional features
from router import Router, RTimer

LocalHost = "127.0.0.1"
ROUTER = None # Router Obj
SOCKETS = {} # Enabled Interfaces

########## Body ##########
def createSocket():
    for port in ROUTER.INPUT_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LocalHost, port))
        SOCKETS[port] = sock

def send(mode):
    """ Send forwarding table to neighbour routers """
    for destID, link in ROUTER.OUTPUT_PORTS.items():
        table = ROUTER.get_routing_table(destID, mode)
        if len(table) == 0:
            # entry may got updated while delay & prepare package
            continue
        message = create_rip_packet(table)
        dest = (LocalHost, link[0])
        SOCKETS[link[2]].sendto(message, dest)

    print(f"Routing Table ({mode}) sent to neighbours at {strCurrTime()}.\n")
    if mode == ROUTER.REGULAR_UPDATE:
        ROUTER.reset_timer(RTimer.PERIODIC_TIMEOUT)
        

def send_periodic():
    mode = "None"
    if ROUTER.is_expired(RTimer.PERIODIC_TIMEOUT, getTime()):
        # Regular update
        mode = ROUTER.REGULAR_UPDATE
    elif ROUTER.has_expired_entry(getTime()):
        # Triggered update. Known NoResponse links don't trigger this
        mode = ROUTER.EXPIRED_UPDATE
    else:
        return

    send(mode)
    
def receive(timeout = 0.013):
    """ Return True if some data received """
    readable, _, _ = select.select(SOCKETS.values(), [], [], timeout)
    for sock in readable:
        receiver = sock.getsockname()
        data, sender = sock.recvfrom(1024)
        if not ROUTER.is_expected_sender(sender, receiver):
            print(f"Droped message on {sender} -> {receiver} link!")
            continue
        routes = process_rip_packet(data)
        print(f"Received ROUTES {str(routes)} at {strCurrTime(getTime())} from {sender}")
        triggered_update = ROUTER.update_route_table(routes, getTime())
        if triggered_update:
            # Next time, the record become Reset Timer
            send(Router.FAST_ROUTE_UPDATE)

def garbage_collection():
    ROUTER.garbage_collection(getTime())

########## Program ##########
def init_router():
    global ROUTER # include this if modifying global variable
    filename = sys.argv[1]
    rID, inputs, outputs, timeout = read_config(filename)

    #  Router instance with default routing table
    ROUTER = Router(rID, inputs, outputs, getTime(True), timeout)
    ROUTER.print_hello()

    # First time notice to neighbours
    createSocket()

if __name__ == "__main__":
    try:
        init_router()
        while True:
            ROUTER.print_route_table(getTime())
            send_periodic()
            garbage_collection()
            receive()

    except IndexError:
        print("Error: Config file is not provided!")
    except FileNotFoundError:
        print("Error: given Config file not found!")
    except ValueError as v_err:
        print("Warning:", v_err)
    except socket.error as s_err:
        print("Error:", s_err)
    except KeyboardInterrupt:
        print("\n******** Daemon exit successfully! Router shuting down... ********")
    except Exception as e:
        traceback.print_exc() # Traceback unknown error
        print("Program exited unexpectedly.\n")
    finally:
        print()
        sys.exit()