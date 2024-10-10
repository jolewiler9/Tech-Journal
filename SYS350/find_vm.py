def find_vm(vm_name):
    try:
        # Searches for the VM in the inventory
        for vm in si.content.rootFolder.childEntity[0].vmFolder.childEntity:
            if vm.name == vm_name:
                return vm
        raise Exception(f"VM {vm_name} not found.")
    except Exception as e:
        print(f"Error finding VM: {e}")
