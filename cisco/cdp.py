import re

def parse(cdp_data):
    'Return nd neighbors for IOS/NXOS cdp output'
    current = dict()
    nd = list()
    for l in re.split("-{5,}",cdp_data):
        l = l.rstrip()
        devid = re.search('Device\sID\:\s*([A-Za-z0-9\.\-\_]+)', l)
        platform = re.search('Platform\:\s([A-Za-z0-9\.\-\_]+)\s*([A-Za-z0-9\.\-\_]*)', l)
        ints = re.search('Interface\:\s([A-Za-z0-9\.\-\_\/]+).*\:\s([A-Za-z0-9\.\-\_\/]+)', l)
        ipv4 = re.search('\s+IPv4\sAddress\:\s(\d+\.\d+\.\d+\.\d+)', l)
        ip = re.search('\s+IP\saddress\:\s(\d+\.\d+\.\d+\.\d+)', l)
        nxos = re.search('Cisco Nexus', l)
        ios = re.search('Cisco IOS', l)
        if devid:
            if current:
                nd.append(current.copy())
            current = dict()
            rname = devid.group(1)
            # current['local_device_id'] = dname
            current['remote_device_id'] = rname
            current['platform'] = 'Unknown'
            current['local_int'] = 'Unknown'
            current['remote_int'] = 'Unknown'
            current['ipv4'] = 'Unknown'
            current['os'] = 'Unknown'
        if ints:
            #print(l, ints.group(1), ints.group(2))
            current['local_int'] = ints.group(1)
            current['remote_int'] = ints.group(2)
        if ipv4:
            current['ipv4'] = ipv4.group(1)
        if ip:
            current['ipv4'] = ip.group(1)
        if platform:
            if platform.group(1) == 'cisco':
                current['platform'] = platform.group(2)
            else:
                current['platform'] = platform.group(1)
        if nxos:
            current['os'] = 'cisco_nxos'
        if ios:
            current['os'] = 'cisco_ios'
    if current:
        nd.append(current.copy())
    return nd
