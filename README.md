# cdp_crawl
Recursive CDP Neigbor discovery with netmiko

Usage: python3 neighbor_map.py

Enter username, password and a seed device.
The script will go out and login via SSH into the seed device and parse the output from 'show cdp neighbor detail'
