"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter (27380476)
Router main program
"""
from timer import RTimer
from deamon_sup import strCurrTime as strtime

class Router:
    def __init__(self, rID, inputs, outputs, startTime, timeout):
        _timeout = timeout if timeout is not None else 20
        self.timer = RTimer(_timeout)
        self._garbages = [] # (dest, time since expired)

        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs

        self._ROUTING_TABLE = {}  # {Dest: nxt Hop, metric, time, path}
        self._ROUTING_TABLE[rID] = [rID, 0, startTime, ["Time Active"]]

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

    def update_route_table(self, routes, utime):
        print(f"Received ROUTES {str(routes)} at {strtime(utime)}")

        for route in routes:
            dest, nxtHop, metric = route
            new_metric = metric + self.OUTPUT_PORTS[nxtHop][1] # link cost to receive
            new_metric = 16 if new_metric > 16 else new_metric

            new_entry = [nxtHop, new_metric, utime.timestamp(), []]
            exist_entry = self._ROUTING_TABLE.get(dest, None)
            
            if exist_entry is None:
                new_entry[-1] = ["New dest."]
            elif new_metric < exist_entry[1]:
                new_entry[-1] = ["Shorter route"]
            elif new_metric == exist_entry[1]:
                if new_entry[0] != exist_entry[0]:
                    new_entry[-1] = ["New route, same cost"]
                else:
                    new_entry[-1] = ["Reset timer"]
            self._ROUTING_TABLE[dest] = new_entry


    def garbage_collection(self, gtime):
        for item, time in self._garbages.copy():
            if self.timer.is_expired(RTimer.GARBAGE_TIMEOUT, gtime, time):
                self._ROUTING_TABLE.pop(item, None)
                self._garbages.remove((item, time))
                print(f"Removed dead link to {item} at {strtime(gtime)}")

    def has_expired_entry(self, etime):
        for dest,entry in self._ROUTING_TABLE.items():
            if dest == self.ROUTER_ID:
                continue

            _, metric, ttl, _ = entry
            if metric == 16:
                continue

            if self.timer.is_expired(RTimer.ENTRY_TIMEOUT, etime, ttl):
                self._ROUTING_TABLE[dest][1] = 16 # set to infinity
                self._garbages.append((dest, ttl))
                print(self._garbages)
                print(self._ROUTING_TABLE)
                print(f"Found expired link to {dest} at {strtime(etime)}")
        return len(self._garbages) < 0

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

    def print_route_table(self, ptime):
        if not self.timer.is_expired(RTimer.PRINT_TIMEOUT, ptime):
            return
            
        print("="*66)
        print("|{:16}--{} [{}]--{:16}|".format(" ", "ROUTING TABLE", strtime(ptime), " "))
        print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^20}|".format(
            "Dest.", "Next Hop", "Metric", "Time (s)", "Notes"))
        print("|" + "-"*64 + "|")
        for dest, record in self._ROUTING_TABLE.items():
            hop, cost, log_time, path = record
            duration = ptime.timestamp() - log_time
            print("|{:^10}|{:^10}|{:^10}|{:^10.3f}|{:^20}|".format(
                dest, hop, cost, duration, str(path)))
        print("="*66)
        self.timer.reset_timer(RTimer.PRINT_TIMEOUT)

    def reset_timer(self, mode):
        self.timer.reset_timer(mode)

    def is_expired(self, mode, curr_time):
        return self.timer.is_expired(mode, curr_time)
