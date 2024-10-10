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
        task_result = wait_for_task(task)
        print(f"Snapshot '{snapshot_name}' created for VM {vm.name}.")
    except Exception as e:
        print(f"Error creating snapshot for VM: {e}")
