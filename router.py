
"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter ()
Router main program
"""

class Router:
    def __init__(self, rID, inputs, outputs, ptime):
        self._lastPrint = -1
        self.TIMEOUT_print = 5

        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs

        self._ROUTING_TABLE = {}  # {Dest: nxt Hop, metric, time, path}
        self._ROUTING_TABLE[rID] = [rID, 0, ptime, []]

        self.OUTPUT_PORTS = {}
        for output in outputs:
            port, cost, dest = output.split('-')
            port, cost, dest = int(port), int(cost), int(dest)
            self.OUTPUT_PORTS[dest] = (port, cost)

    def get_routing_table(self, dest):
        entries = []
        for key, val in self._ROUTING_TABLE.items():
            if dest != key:
                entries.append((key, self.ROUTER_ID, val[1]))
        return entries

    def update_route_table(self, routes, time):
        """ Just testing """

        print(routes, "ROUTES LIST")

        is_updated = False # True if at least 1 entry updated
        for route in routes:
            dest, nxtHop, metric = route
            new_metric = metric + self.OUTPUT_PORTS[nxtHop][1] # link cost to receive
            new_metric = 16 if new_metric > 16 else new_metric

            new_entry = [nxtHop, new_metric, time, []]
            exist_entry = self._ROUTING_TABLE.get(dest, None)
            
            if exist_entry is None:
                new_entry[-1] = ["New dest."]
                self._ROUTING_TABLE[dest] = new_entry
                is_updated = True
            elif new_metric < exist_entry[1]:
                new_entry[-1] = ["Shorter route"]
                self._ROUTING_TABLE[dest] = new_entry
                is_updated = True
            elif new_metric == exist_entry[1]:
                new_entry[-1] = ["Reset timer"]
                if new_entry[0] != exist_entry[0]:
                    new_entry[-1] = ["New route, same cost"]
                    is_updated = True
                self._ROUTING_TABLE[dest] = new_entry
                # If not new route (just reset timer) then don't raise updat flag

        return is_updated

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
            if (ptime - self._lastPrint) < self.TIMEOUT_print:
                return

        print("="*66)
        print("|{:19}{} [{}]  {:19}|".format(" ", "ROUTING TABLE", strtime, " "))
        print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^20}|".format(
            "Dest.", "Next Hop", "Metric", "Time (s)", "Notes"))
        print("|" + "-"*64 + "|")
        for dest, record in self._ROUTING_TABLE.items():
            hop, cost, log_time, path = record
            duration = ptime - log_time
            print("|{:^10}|{:^10}|{:^10}|{:^10.3f}|{:^20}|".format(
                dest, hop, cost, duration, str(path)))
            record[3] = []
        print("="*66)
        self._lastPrint = ptime

