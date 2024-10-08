import time
from pyVmomi import vim

def find_network(network_name):
    for network in si.content.rootFolder.childEntity[0].network:
        if network.name == network_name:
            return network
    raise Exception(f"Network {network_name} not found.")
