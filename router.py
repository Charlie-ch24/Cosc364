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
        self.ROUTING_TABLE[rID] = [rID, 0, 0, None]

        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            self.OUTPUT_PORTS[int(dest)] = (int(port), int(cost))

    def print_hello(self):      
        print("-" * 50)  
        print("Router {0} is running ...".format(self.ROUTER_ID))
        print("Input ports:", self.INPUT_PORTS)
        print("Output ports:")
        for dest, link in self.OUTPUT_PORTS.items():
            print("    {0} to Router ID {1}".format(link,dest))
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






