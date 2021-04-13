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

TIMEOUT_send = [2, 10] # Min (random), max
TIMEOUT_link = TIMEOUT_send[1] * 6

Last_sent = -1
Update_Flag = False

########## Body ##########
def createSocket():
    for port in ROUTER.INPUT_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LocalHost, port))
        SOCKETS.append(sock)

def send(is_updated):
    """ Send forwarding table to neighbour routers """
    global Last_sent, Update_Flag
    status = "No-change"
    if is_updated is None:
        status = "Default"
    elif is_updated:
        status = "Updated"
        if (time.time() - Last_sent) < TIMEOUT_send[0]:
            TIMEOUT_send[0] = random.randint(0,2)
            return
    else:
        if (time.time() - Last_sent) < TIMEOUT_send[1]:
            return

    message = bytearray([ROUTER.ROUTER_ID, 0x2, 0x9])
    for _, link in ROUTER.OUTPUT_PORTS.items():
        dest = (LocalHost, link[0])
        for sock in SOCKETS:
            sock.sendto(message, dest)
    
    Last_sent = time.time()
    Update_Flag = False 
    print(f"Routing Table ({status}) sent to neighbours at {time.strftime('%X')}.\n")

def receive(timeout = 1):
    """ return True if some data received """
    readable, _, _ = select.select(SOCKETS, [], [], timeout)
    # update_count = 0
    # for sock in readable:
    #     data, sender = sock.recvfrom(1024)
    #     if not ROUTER.is_expected_sender(sender):
    #         print(f"Droped message on {sender} -> {sock.getsockname()} link!")
    #         pass
    #     else:
    #         print(f"Accepted message on {sender} -> {sock.getsockname()} link!")
    #         print(data)
    #         routes = system.process_Rip_adv(data)
    #         is_updated = ROUTER.update_route_table(routes)
    #         if is_updated:
    #             update_count += 1
    # return True if update_count > 0 else False

    routes = [
        [7, 1, 1, 0.5, [7, 1]], 
        [2, 7, 15, 0.5, [7, 1]],
        [2, 7, 1, 0.5, [7, 1]]
    ]
    is_updated = ROUTER.update_route_table(routes)
    return is_updated

########## Program ##########
def init_router():
    global ROUTER # include this if modifying global variable
    filename = sys.argv[1]
    rID, inputs, outputs = system.read_config(filename)

    # Create Router instance with default routing table
    timestamp = time.time()
    ROUTER = Router(rID, inputs, outputs, timestamp)
    ROUTER.print_hello()

    # First time notice to neighbours
    createSocket()
    ROUTER.print_route_table(True, timestamp, time.strftime('%X'))
    send(None) # periodic every 30 sec
    
if __name__ == "__main__":
    try:
        init_router()
        while True:
            just_updated = receive()
            Update_Flag = just_updated if not Update_Flag else Update_Flag
            ROUTER.print_route_table(just_updated, time.time(), time.strftime('%X'))
            send(Update_Flag)

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
