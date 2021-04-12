"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""
import random

class Router:
    def __init__(self, rID, inputs, outputs):
        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs

        self.ROUTING_TABLE = {} # {Dest: nxt Hop, metric, time, path}
        self.ROUTING_TABLE[rID] = [rID, 0, 0, None]

        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            self.OUTPUT_PORTS[int(dest)] = (int(port), int(cost))

    def update_route_table(self, routes):
        """ Just testing """
        flag = random.randint(0, 1)
        if flag == 0:
            rID = random.randint(1,7)
            self.ROUTING_TABLE[7] = [rID, 7-rID, 0, None]
            return True
        return False

    def print_hello(self):      
        print("-" * 50)  
        print(f"Router {self.ROUTER_ID} is running ...")
        print("Input ports:", self.INPUT_PORTS)
        print("Output ports:")
        for dest, link in self.OUTPUT_PORTS.items():
            print(f"    {link} to Router ID {dest}")
        print("-" * 50)
        print("Use Ctrl+C or Del to shutdown.")        
        print()

    def print_route_table(self):
        column = "|{:^10}|{:^10}|{:^10}|{:^10}|{:^20}|"
        print("="*66)
        print("{:25}{}{:25}".format(" ", "ROUTING TABLE", " "))
        print(column.format(
            "Dest.", "Next Hop", "Cost", "Time", "Path"))
        print("-"*66)
        for dest, record in self.ROUTING_TABLE.items():
            hop, cost, time, path = record
            print(column.format(dest, hop, cost, time, str(path)))

        print("="*66)






