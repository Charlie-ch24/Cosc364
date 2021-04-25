"""
Assignment 1: RIP protocol
Team: Bach Vu (25082165), Charlie Hunter (27380476)
Router main program
"""
from timer import RTimer
from daemon_sup import strCurrTime

class Router:
    def __init__(self, rID, inputs, outputs, startTime, timeout):
        _timeout = timeout if timeout is not None else 5
        self.timer = RTimer(_timeout)
        self._garbages = {} # (dest, time since expired)

        self.ROUTER_ID = rID
        self.INPUT_PORTS = inputs

        self._ROUTING_TABLE = {}  # {Dest: nxt Hop, metric, time, path}
        self._ROUTING_TABLE[rID] = ["-", 0, startTime, ["Time Active"]]

        self.OUTPUT_PORTS = {} # (dest, cost, port_to_send)
        for output in outputs:
            from_port, to_port, cost, dest = output.split('-')
            from_port, to_port, cost, dest = int(from_port), int(to_port), int(cost), int(dest)
            self.OUTPUT_PORTS[dest] = (to_port, cost, from_port)

    def get_routing_table(self, dest):
        entries = []
        for key, val in self._ROUTING_TABLE.items():
            if dest == val[0]:
                # don't re-advertise info from a hop
                continue
            entries.append((key, self.ROUTER_ID, val[1]))
        return entries

    def update_route_table(self, routes, utime):
        print(f"Received ROUTES {str(routes)} at {strCurrTime(utime)}")
        for route in routes:
            dest, nxtHop, metric = route
            new_metric = metric + self.OUTPUT_PORTS[nxtHop][1] # link cost to receive
            if metric < 16 and new_metric >= 16:
                # unreachable, deadlink update will have metric = 16
                continue

            new_metric = 16 if new_metric > 16 else new_metric            
            new_entry = [nxtHop, new_metric, utime.timestamp(), []]
            exist_entry = self._ROUTING_TABLE.get(dest, None)            
            
            if not self._need_update(new_entry, exist_entry):
                continue

            self._ROUTING_TABLE[dest] = new_entry
            # updated dest entry could be in garbage collecting
            self._garbages.pop(dest, None)

    def _need_update(self, new_entry, exist_entry):
        """ For fancy purpose of taking note when update an entry 
            return True if new entry is valid to be updated
        """
        if exist_entry is None:
            if new_entry[1] == 16:
                # Don't worry about dead link of unknown dest
                return False 
            new_entry[3] = ["New dest."]
        else:
            if new_entry[1] < exist_entry[1]:
                new_entry[3] = ["Shorter route"]
            
            elif new_entry[1] == 16:
                if exist_entry[1] == 16:
                    # already receive this link dead
                    return False 
                elif exist_entry[0] != new_entry[0]:
                    # link dead is not currently in route table
                    return False  
                # 1st time known dest (metric < 16) has dead link
                new_entry[3] = ["Link dead."]
            
            elif new_entry[1] == exist_entry[1]:
                new_entry[3] = ["Reset timer"]
                if new_entry[0] != exist_entry[0]:
                    # New route, reset timer still
                    new_entry[3] = ["Same cost"] 
            
            else:
                # ["Slower route."], not update
                return False

        return True 

    def garbage_collection(self, gtime):
        for item, time in self._garbages.copy().items():
            if self.timer.is_expired(RTimer.GARBAGE_TIMEOUT, gtime, time):
                self._ROUTING_TABLE.pop(item, None)
                self._garbages.pop(item)
                print(f"Removed dead link to {item} at {strCurrTime(gtime)}")

    def has_expired_entry(self, etime):
        for dest,entry in self._ROUTING_TABLE.items():
            if dest == self.ROUTER_ID:
                continue

            _, metric, ttl, _ = entry
            if metric == 16:
                if dest in self._garbages.keys():
                    # Waiting to be removed
                    continue
                self._garbages[dest] = etime.timestamp()

            elif self.timer.is_expired(RTimer.ENTRY_TIMEOUT, etime, ttl):
                entry[1], entry[-1] = 16, ["No response."]
                self._ROUTING_TABLE[dest][1] = 16 # set to infinity
                self._garbages[dest] = etime.timestamp()
                print(f"Found expired link to {dest} at {strCurrTime(etime)}")
        return len(self._garbages) < 0

    def is_expected_sender(self, sender, receiver):
        for link in self.OUTPUT_PORTS.values():
            if sender[1] == link[0] and receiver[1] == link[2]:
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
        print("|{:16}--{} [{}]--{:16}|".format(" ", "ROUTING TABLE", strCurrTime(ptime), " "))
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

