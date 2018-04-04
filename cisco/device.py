from . import cdp
from netmiko import ConnectHandler

def get_neighbors(host, username, password, device_type):
    try:
        sw = ConnectHandler(device_type=device_type, ip=host, username=username, password=password)
    except:
        print("Could not connect to " + host)
        raise
    else:
        print("Connected to " + host)
        cdp_detail = sw.send_command("sh cdp neighbors detail")
        return cdp.parse(cdp_detail)
