import netifaces

def default_gateway():
    gws = netifaces.gateways()
    return gws["default"][netifaces.AF_INET][0]
