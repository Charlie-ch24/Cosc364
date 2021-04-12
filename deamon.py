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


def router_id_check(Rid):

    if int(Rid) in range(1, 64000):
        print("Works")
        return Rid
    else:
        print("Error: Invaild router id")
        sys.exit()


def inputport_check(inputs):

    valid_check = []
    for input in inputs:
        if int(input) in range(1024, 64000) and int(input) not in valid_check:
            valid_check.append(input)
            print("yay input")
        else:
            print("Error: Invaild port numbers")
            sys.exit()
            break
    return valid_check

def output_check(outputs, valid_input):

    output_info ={}
    for output in outputs:
        port, value, dest_id = output.split('-')
        port = port
        value = int(value)
        dest_id = int(dest_id)
        if int(port) in range(1024, 64000):
            for valid in valid_input:
                if int(valid) == int(port):
                    print("Output should not be an input")
                    print(port, valid_input)
                    sys.exit()
                else:
                    print("yay output")
                    output_info[port] = [value, dest_id]

        else:
            print("Error: output port out of range")
            sys.exit()

    return output_info







########## Program ##########
def main():
    global ROUTER
    try:
        filename = sys.argv[1]
        rID, inputs, outputs = system.read_config(filename)
        rID = router_id_check(rID)
        inputs = inputport_check(inputs)
        output = output_check(outputs, inputs)
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
