import getpass
import json
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

# Load vCenter credentials from json file
with open("vcenter_config.json") as config_file:
    config = json.load(config_file)
vcenter_host = config['vcenter'][0]['vcenterhost']
vcenter_user = config['vcenter'][0]['vcenteradmin']

# Prompt for password securely
vcenter_pass = getpass.getpass(prompt='Enter your vCenter password: ')

# Set up SSL context to ignore cert errors (for simplicity in development)
s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s.verify_mode = ssl.CERT_NONE

# Connect to vCenter
si = SmartConnect(host=vcenter_host, user=vcenter_user, pwd=vcenter_pass, sslContext=s)

# Get aboutInfo from the session
about_info = si.content.about
print("Connected to vCenter: " + about_info.fullName)

# Extract domain/username and source IP from session
user_info = si.content.sessionManager.currentSession
print(f"Logged in as: {user_info.userName}")
print(f"Source IP Address: {user_info.ipAddress}")
print(f"vCenter Server: {vcenter_host}")

# Function to search VMs by name
def search_vms(name_filter=None):
    vm_view = si.content.viewManager.CreateContainerView(si.content.rootFolder, [vim.VirtualMachine], True)
    vms = vm_view.view

    # Filter VMs by name if a filter is provided
    if name_filter:
        vms = [vm for vm in vms if name_filter.lower() in vm.name.lower()]

    # Iterate over all VMs and print required metadata
    for vm in vms:
        summary = vm.summary
        print(f"VM Name: {summary.config.name}")
        print(f"Power State: {summary.runtime.powerState}")
        print(f"CPUs: {summary.config.numCpu}")
        print(f"Memory: {summary.config.memorySizeMB / 1024} GB")
        if summary.guest is not None:
            print(f"IP Address: {summary.guest.ipAddress}")
        print("-----------")

# Get user input for VM name search (leave empty for all VMs)
vm_name = input("Enter a VM name to search (leave blank to list all VMs): ")
search_vms(name_filter=vm_name)
