"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""
########## Header ##########
import deamon_sup as system
import socket, select
import sys, time, random, traceback
from router import *

LocalHost = "127.0.0.1"
ROUTER = None # Router Obj

########## Body ##########










########## Program ##########
def init_router():
    global ROUTER
    filename = sys.argv[1]
    rID, inputs, outputs = system.read_config(filename)
    ROUTER = Router(rID, inputs, outputs)
    ROUTER.print_hello()    
    
if __name__ == "__main__":
    try:
        init_router()
        while True:
            ROUTER.print_route_table()
            time.sleep(3)
    except IndexError:
        print("Error: Config file is not provided!")
    except FileNotFoundError:
        print("Error: given Config file not found!")
    except ValueError as v_err:
        print("Warning:", v_err)
    except KeyboardInterrupt:
        print("\n***** Deamon exit successfully! Router shuting down... *****")
    except Exception as e:
        traceback.print_exc() # Traceback unknown error
        print("Program exited unexpectedly.\n")
    finally:
        sys.exit()
