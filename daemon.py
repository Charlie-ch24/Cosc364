"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter (27380476)
Router main program
"""
########## Header ##########
import daemon_sup as system
from daemon_sup import getTime
import socket, time, select
import sys, random # must use
import traceback # optional features
from router import Router, RTimer

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
            fId = link[2]
            if fId == sock.getsockname()[1]:
                sock.sendto(message, dest)
                break

async def send_periodic():
    """ Execute periodically """
    if ROUTER.has_expired_entry(getTime()):
        await asyncio.sleep(ROUTER.get_update_delay())
        print(f"Routing Table (expiry) sent to neighbours at {system.strCurrTime()}.\n")
    elif ROUTER.is_expired(RTimer.PERIODIC_TIMEOUT, getTime()):
        print(f"Routing Table (periodic) sent to neighbours at {system.strCurrTime()}.\n")
    else:
        return
    send()
    ROUTER.reset_timer(RTimer.PERIODIC_TIMEOUT) # Reset timer after sent to all neighbour

def receive(timeout = 0.1):
    """ Return True if some data received """
    readable, _, _ = select.select(SOCKETS, [], [], timeout)
    for sock in readable:
        data, sender = sock.recvfrom(1024)
        print(data)
        if not ROUTER.is_expected_sender(sender):
            print(f"Droped message on {sender} -> {sock.getsockname()} link!")
            continue
        routes = system.process_rip_packet(data)
        ROUTER.update_route_table(routes, getTime())

########## Program ##########
def init_router():
    global ROUTER # include this if modifying global variable
    filename = sys.argv[1]
    rID, inputs, outputs, timeout = system.read_config(filename)

    #  Router instance with default routing table
    ROUTER = Router(rID, inputs, outputs, getTime(True), timeout)
    ROUTER.print_hello()

    # First time notice to neighbours
    createSocket()

    ROUTER.print_route_table()
    # await send_periodic()

TASKS = []
async def print_async():
    while True:
        ROUTER.print_route_table()
        await asyncio.sleep(1)

async def garbage_async():
    ROUTER.garbage_collection(getTime())

async def main():
    """ start processing task at the same time """
    # global TASKS
    # if len(TASKS) == 0:
    #     await init_router()
    #     # print_task = asyncio.create_task(print_async())
    #     # send_task = asyncio.create_task(send_periodic())
    #     # garbage_task = asyncio.create_task(garbage_async())
    #     # TASKS = [print_task, send_task, garbage_task]
    #     TASKS = [None]
    #     return
    
    # Initialize tasks
    await init_router()
    print_task = asyncio.create_task(print_async())
    send_task = asyncio.create_task(send_periodic())
    garbage_task = asyncio.create_task(garbage_async())
    
    # Exceute Tasks
    while True:
        await print_task
        await send_task
        await garbage_task
        receive()
    # await TASKS[0]
    # await TASKS[1]
    # await TASKS[2]

if __name__ == "__main__":
    mainloop = asyncio.get_event_loop()
    try:
        init_router()
        asyncio.ensure_future(print_async())
        mainloop.run_forever()
        # while True:
        #     mainloop.run_until_complete(main())
        #     asyncio.run(mainloop())

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
        mainloop.close()
        sys.exit()