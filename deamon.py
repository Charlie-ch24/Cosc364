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
def main():
    global ROUTER
    try:
        filename = sys.argv[1]
        rID, inputs, outputs = system.read_config(filename)
        ROUTER = Router(rID, inputs, outputs)
    except IndexError:
        print("Error: Config file is not provided!")
    except FileNotFoundError:
        print("Error: given Config file not found!")
    except ValueError:
        print("Error: Invalid port number in config data")
    except Exception:
        raise Exception
    else:
        # No exception
        ROUTER.print_hello()
    
    
if __name__ == "__main__":
    try:
        main()
        while True:
            ROUTER.print_route_table()
            time.sleep(3)
    except KeyboardInterrupt:
        print("Program exited!")
    except Exception as e:
        traceback.print_exc() # Traceback unknown error
        print(e)
        print("Program exited unexpectedly.\n")
    finally:
        sys.exit()
