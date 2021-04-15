# Cosc364

Assignment 1 RIP protocol
Bach Vu: 25082165
Charlie Hunter: 27380476

## Run command

### Window

- cd C:\Users\User\OneDrive\myUC data\Courses\Cosc364
- Demo: `python deamon.py config_demo/router1`
- Test: `python deamon.py config_test/test1`

### MAC OS

- cd C:/usr/local/bin/python3.8 "/Users/charliehunter/Desktop/cosc364/Cosc364
- python deamon.py config_demo/router1

### Linux

- Locate Project folder -> Right click -> Open in Terminal
- Demo: `python3 deamon.py config_demo/router1`
- Test: `python3 deamon.py config_test/test1`

## GIT command

- Remove track folder: git rm -r --cached `folder/file`

## Test cases (/config_test)

- Use test command (from Commands above)

| Test file | Content |
|-----------|---------|
| `random`  | Config file not exist     |
| `test1a`  | Invalid Router ID         |
| `test1b`  | Invalid Router Input port |
| `test1c`  | Invalid Router Output port|
| `test2a`  | Missing 1 mandatory field |
| `test2b`  | Missing mandatory fields  |

## Documatation

- RIPv2 dont have request packet, only send its routing table as distance-vector. Thus `Command` and `Version` field will be constant (0 and 2).
- If Equal cost happen, and timer of existing record is half-way to time out, update to new route (3.9 pg 28). Thus at most 1 destination at a time.
- Assume link cost (from config) is hop metric.
- Implement triggered updates only when routes become invalid (i.e. when a router
sets the routes metric to 16 for whatever reason, compare end of page 24 and
beginning of page 25 in [1]), not for other metric updates or new routes.
