def change_vm_network():
    try:
        vm_name = input("Enter the name of the VM to change its network: ")
        vm = find_vm(vm_name)
        new_network_name = input("Enter the name of the new network: ")
        print(f"Changing network for VM: {vm.name}")
        
        device_change = []
        network = find_network(new_network_name)

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                print(f"Updating network on device: {device.deviceInfo.label}")
                nic_spec = vim.vm.device.VirtualDeviceSpec()
                nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                nic_spec.device = device
                nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo(network=network)
                device_change.append(nic_spec)

        spec = vim.vm.ConfigSpec(deviceChange=device_change)
        task = vm.ReconfigVM_Task(spec=spec)
        task_result = wait_for_task(task)
        print(f"VM {vm.name} network changed to {new_network_name}.")
    except Exception as e:
        print(f"Error changing network for VM: {e}")
