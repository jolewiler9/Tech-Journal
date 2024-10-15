import getpass
import json
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import time

# Load vCenter credentials from JSON file
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

# Function to wait for task completion
def wait_for_task(task):
    while task.info.state == vim.TaskInfo.State.running:
        print("Task is still running...")
        time.sleep(2)
    if task.info.state == vim.TaskInfo.State.success:
        print("Task completed successfully!")
        return task.info.result
    else:
        print(f"Task failed with error: {task.info.error}")
        raise task.info.error

# Function to find a VM by name
def find_vm(vm_name):
    for vm in si.content.rootFolder.childEntity[0].vmFolder.childEntity:
        if vm.name == vm_name:
            return vm
    raise Exception(f"VM {vm_name} not found.")
    
# Function to find a network by name
def find_network(network_name):
    for network in si.content.rootFolder.childEntity[0].network:
        if network.name == network_name:
            return network
    raise Exception(f"Network {network_name} not found.")

# Function to power on a VM
def power_on_vm():
    try:
        vm_name = input("Enter the name of the VM you want to power on: ")
        vm = find_vm(vm_name)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
            print(f"Powering on VM: {vm.name}")
            task = vm.PowerOn()
            wait_for_task(task)
            print(f"VM {vm.name} has been powered on.")
        else:
            print(f"VM {vm.name} is already powered on.")
    except Exception as e:
        print(f"Error powering on VM: {e}")

# Function to power off a VM
def power_off_vm():
    try:
        vm_name = input("Enter the name of the VM you want to power off: ")
        vm = find_vm(vm_name)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            print(f"Powering off VM: {vm.name}")
            task = vm.PowerOff()
            wait_for_task(task)
            print(f"VM {vm.name} has been powered off.")
        else:
            print(f"VM {vm.name} is already powered off.")
    except Exception as e:
        print(f"Error powering off VM: {e}")

# Function to create a snapshot of a VM
def create_vm_snapshot():
    try:
        vm_name = input("Enter the name of the VM you want to snapshot: ")
        vm = find_vm(vm_name)
        snapshot_name = input("Enter a name for the snapshot: ")
        description = input("Enter a description for the snapshot (optional): ") or "Snapshot created by pyvmomi script"
        
        dump_memory = input("Do you want to include the VM's memory in the snapshot? (yes/no): ").lower() == 'yes'
        quiesce = input("Do you want to quiesce the VM's file system? (yes/no): ").lower() == 'yes'
        
        print(f"Creating snapshot for VM: {vm.name}")
        task = vm.CreateSnapshot_Task(name=snapshot_name, description=description, memory=dump_memory, quiesce=quiesce)
        wait_for_task(task)
        print(f"Snapshot '{snapshot_name}' created for VM {vm.name}.")
    except Exception as e:
        print(f"Error creating snapshot for VM: {e}")

# Function to restore the latest snapshot
def restore_latest_snapshot():
    try:
        vm_name = input("Enter the name of the VM to restore the latest snapshot: ")
        vm = find_vm(vm_name)
        snapshot = vm.snapshot
        if snapshot is not None:
            latest_snapshot = snapshot.rootSnapshotList[-1]  # Gets the latest snapshot
            print(f"Restoring latest snapshot for VM: {vm.name}")
            task = latest_snapshot.snapshot.RevertToSnapshot_Task()
            wait_for_task(task)
            print(f"VM {vm.name} restored to the latest snapshot.")
        else:
            print(f"VM {vm.name} has no snapshots to restore.")
    except Exception as e:
        print(f"Error restoring snapshot for VM: {e}")

# Function to change the network of a VM
def change_vm_network():
    try:
        vm_name = input("Enter the name of the VM to change its network: ")
        vm = find_vm(vm_name)
        new_network_name = input("Enter the name of the new network: ")
        network = find_network(new_network_name)  # Find the new network
        
        print(f"Changing network for VM: {vm.name}")
        device_change = []  # List to hold device changes

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                print(f"Updating network on device: {device.deviceInfo.label}")
                
                nic_spec = vim.vm.device.VirtualDeviceSpec()
                nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                nic_spec.device = device
                nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo(network=network)
                
                device_change.append(nic_spec)  # Add the NIC specification to the list

        if device_change:  # Ensure there are changes to apply
            spec = vim.vm.ConfigSpec(deviceChange=device_change)  # Create a ConfigSpec with all changes
            task = vm.ReconfigVM_Task(spec=spec)  # Apply the changes
            wait_for_task(task)  # Wait for the task to complete
            print(f"VM {vm.name} network changed to {new_network_name}.")
        else:
            print("No network changes were made.")

    except Exception as e:
        print(f"Error changing network for VM: {e}")

# Function to delete a VM
def delete_vm():
    try:
        vm_name = input("Enter the name of the VM you want to delete: ")
        vm = find_vm(vm_name)
        confirm = input(f"Are you sure you want to delete {vm.name} from disk? This action cannot be undone. (yes/no): ").lower()
        if confirm == 'yes':
            print(f"Deleting VM: {vm.name}")
            task = vm.Destroy_Task()
            wait_for_task(task)
            print(f"VM {vm.name} has been deleted from disk.")
        else:
            print("VM deletion aborted.")
    except Exception as e:
        print(f"Error deleting VM: {e}")

# Main function to drive the script
def main():
    while True:
        print("\nVM Management Menu")
        print("1. Power On VM")
        print("2. Power Off VM")
        print("3. Create Snapshot")
        print("4. Restore Latest Snapshot")
        print("5. Change VM Network")
        print("6. Delete VM")
        print("0. Exit")
        
        choice = input("Choose an option: ")
        if choice == '1':
            power_on_vm()
        elif choice == '2':
            power_off_vm()
        elif choice == '3':
            create_vm_snapshot()
        elif choice == '4':
            restore_latest_snapshot()
        elif choice == '5':
            change_vm_network()
        elif choice == '6':
            delete_vm()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please select again.")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
