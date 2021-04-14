
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

        self._ROUTING_TABLE = {} # {Dest: nxt Hop, metric, time, path}
        self._ROUTING_TABLE[rID] = [rID, 1, ptime, [rID]]

        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            port, cost, dest = int(port), int(cost), int(dest)
            self.OUTPUT_PORTS[dest] = (port, cost)
        self.DISCOVER = {}
        self.DISCOVER = self.OUTPUT_PORTS


    def get_routing_table(self):
        entries = []
        for key, val in self._ROUTING_TABLE.items():
            entries.append((key, val[0], val[1]))
        return entries

    def update_route_table(self, routes):
        """ Just testing """

        print(routes, "ROUTES LIST")
        #print(self._ROUTING_TABLE, "ROUTING TABLE")
        print(self.OUTPUT_PORTS, "OUTPORTS")
        print(self.INPUT_PORTS)
        #print(self.DISCOVER, "Discover")

        for route in routes:
            i = -1
            i += 1
            if route[0] not in self._ROUTING_TABLE:
                try:
                    cost = self.OUTPUT_PORTS[route[0]][1]
                    self._ROUTING_TABLE[route[0]] = [route[1], cost, 24, [route[0], routes[i-1][i]]]
                except:
                    #print(route[0], route[2], "EXCEPT STATE")
                    self.DISCOVER[route[0]] = (route[0], route[2])
                    cost = self.OUTPUT_PORTS[route[0]][1] + routes[i-1][2]
                    self._ROUTING_TABLE[route[0]] = [route[0], cost, 1, 1]
                    #print(self._ROUTING_TABLE)

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
        for dest, record in self._ROUTING_TABLE.items():
            hop, cost, log_time, path = record
            duration = ptime - log_time
            print("|{:^10}|{:^10}|{:^10}|{:^10.3f}|{:^20}|".format(
                dest, hop, cost, duration, str(path)))
        print("="*66)
        self._lastPrint = ptime

