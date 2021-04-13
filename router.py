"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""

TIMEOUT_print = 5
class Router:
    def __init__(self, rID, inputs, outputs, ptime):
        self._lastPrint = -1
        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs

        self.ROUTING_TABLE = {} # {Dest: nxt Hop, metric, time, path}
        self.ROUTING_TABLE[rID] = [rID, 1, ptime, [rID]]

        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            port, cost, dest = int(port), int(cost), int(dest)
            self.OUTPUT_PORTS[dest] = (port, cost)

    def update_route_table(self, routes):
        """ Just testing """
        #route = routes[0]
        #self.ROUTING_TABLE[route[0]] = route[1:]
        #self.ROUTING_TABLE[route[0]] = routes[1:]

        print(self.ROUTING_TABLE, "not added")

        for route in routes:
            if route[0] not in self.ROUTING_TABLE:
                self.ROUTING_TABLE[route[0]] = [route[1], route[2], route[3], route[4]]
                print(self.ROUTING_TABLE, "added")
            if route[0] in self.ROUTING_TABLE:
                if route[2] < self.ROUTING_TABLE[route[0]][1]:
                    self.ROUTING_TABLE[route[0]] = [route[1], route[2], route[3], route[4]]
                    print(self.ROUTING_TABLE, "added again")

        return True






        return True

    def is_expected_sender(self, sender):
        for link in self.OUTPUT_PORTS.values():
            if sender == ("127.0.0.1", link[0]):
                return True
        return False

    def print_hello(self):      
        print("-"*66)  
        print(f"Router {self.ROUTER_ID} is running ...")
        print("Input ports:", self.INPUT_PORTS)
        print("Output ports:")
        for dest, link in self.OUTPUT_PORTS.items():
            print(f"    {link} to Router ID {dest}")
        print("-"*66)
        print("Use Ctrl+C or Del to shutdown.")        
        print()

    def print_route_table(self, is_updated, ptime, strtime):
        if not is_updated:
            if (ptime - self._lastPrint) < TIMEOUT_print:
                return

        print("="*66)
        print("|{:19}{} [{}]  {:19}|".format(" ", "ROUTING TABLE", strtime, " "))
        print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^20}|".format(
            "Dest.", "Next Hop", "Metric", "Time (s)", "Path"))
        print("|" + "-"*64 + "|")
        for dest, record in self.ROUTING_TABLE.items():
            hop, cost, log_time, path = record
            duration = ptime - log_time
            print("|{:^10}|{:^10}|{:^10}|{:^10.3f}|{:^20}|".format(
                dest, hop, cost, duration, str(path)))
        print("="*66)
        self._lastPrint = ptime






