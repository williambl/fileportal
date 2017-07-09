import miniupnpc


def new_upnp():
    u = miniupnpc.UPnP()
    u.discover()
    u.selectigd()

    return u

def forward_port(upnp, port):
    portforwarded = upnp.addportmapping(port, 'TCP', upnp.lanaddr, port,
                                        'fileportal', '')
    print(portforwarded)
    return portforwarded

def close_port(upnp, port):
    portclosed = u.deleteportmapping(port, 'TCP')
    return portclosed
