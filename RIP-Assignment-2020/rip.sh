#!/bin/sh

python3 rip.py &
gnome-terminal -e "python3 rip.py demo-config1.txt"
gnome-terminal -e "python3 rip.py demo-config2.txt"
gnome-terminal -e "python3 rip.py demo-config3.txt"
gnome-terminal -e "python3 rip.py demo-config4.txt"
gnome-terminal -e "python3 rip.py demo-config5.txt"
gnome-terminal -e "python3 rip.py demo-config6.txt"
gnome-terminal -e "python3 rip.py demo-config7.txt"

