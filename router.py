"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""

class Router:
    def __init__(self, rID, inputs, outputs):
        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs
        self.ROUTING_TABLE = {}
        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            self.OUTPUT_PORTS[int(dest)] = (int(port), int(cost))

    def print_hello(self):      
        print("-" * 40)  
        print(f"Router {self.ROUTER_ID} is running ...")
        print("Input ports:", self.INPUT_PORTS)
        print("Output ports:")
        for dest, link in self.OUTPUT_PORTS.items():
            print(f"    {link} to Router ID {dest}")
        print("-" * 40)

    def print_route_table(self):
        pass