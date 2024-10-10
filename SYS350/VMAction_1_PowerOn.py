def power_on_vm():
    try:
        vm_name = input("Enter the name of the VM you want to power on: ")
        vm = find_vm(vm_name)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
            print(f"Powering on VM: {vm.name}")
            task = vm.PowerOn()
            task_result = wait_for_task(task)
            print(f"VM {vm.name} has been powered on.")
        else:
            print(f"VM {vm.name} is already powered on.")
    except Exception as e:
        print(f"Error powering on VM: {e}")
