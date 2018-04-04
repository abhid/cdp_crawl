from host import gateway
from cisco import device
import getpass
import pprint
import csv

# Get Default gateway and add to list
def_gw = gateway.default_gateway()

user = input("Username:")
pwd = getpass.getpass(prompt="Password:")
core = input("Seed switch IP:")

# All devices to be parsed
dev_queue = list()

# Uncomment the next line to start with your default gateway
# dev_queue.append(def_gw)

dev_queue.append(core)

discovered_neighbors = list()

# All devices already visited
visited = list()

# Scrape and parse items from the parsing queue if they are not already visited
while len(dev_queue) > 0:
    cur_dev = dev_queue.pop()
    if cur_dev not in visited:
        try:
            # Change cisco_xe to cisco_ios if you don't have ISO XE devices
            cur_neighbors = device.get_neighbors(cur_dev, user, pwd, "cisco_xe")
            for neighbor in cur_neighbors:
                neighbor["local_device_id"] = cur_dev
                if neighbor["ipv4"] != "Unknown":
                    dev_queue.append(neighbor["ipv4"])
            visited.append(cur_dev)
            discovered_neighbors.extend(cur_neighbors)
        except:
            pass

with open('neighbors.csv', 'w') as csvfile:
    fieldnames = ['remote_device_id', 'platform', 'local_int', 'remote_int', 'ipv4', 'os', 'local_device_id']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for neighbor in discovered_neighbors:
        writer.writerow({'remote_device_id':neighbor['remote_device_id'],
                        'platform':neighbor['platform'],
                        'local_int':neighbor['local_int'],
                        'remote_int':neighbor['remote_int'],
                        'ipv4':neighbor['ipv4'],
                        'os':neighbor['os'],
                        'local_device_id':neighbor['local_device_id']})
# pprint.pprint(discovered_neighbors)
