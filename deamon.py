"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""
########## Header ##########
import deamon_sup as system
import socket, select
import sys, time, random
from router import *

LocalHost = "127.0.0.1"
ROUTER = None # Router Obj

########## Body ##########










########## Program ##########
def main():
    try:
        filename = sys.argv[1]
        rID, inputs, outputs = system.read_config(filename)
        ROUTER = Router(rID, inputs, outputs)
    except IndexError:
        print("Error: Config file is not provided!")
    except FileNotFoundError:
        print("Error: given Config file not found!")
    except Exception as e:
        print(e)
    else:
        ROUTER.print_hello()




        
    finally:
        sys.exit()
    
    

main()