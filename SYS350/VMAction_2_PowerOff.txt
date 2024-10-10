def power_off_vm():
    try:
        vm_name = input("Enter the name of the VM you want to power off: ")
        vm = find_vm(vm_name)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            print(f"Powering off VM: {vm.name}")
            task = vm.PowerOff()
            task_result = wait_for_task(task)
            print(f"VM {vm.name} has been powered off.")
        else:
            print(f"VM {vm.name} is already powered off.")
    except Exception as e:
        print(f"Error powering off VM: {e}")
