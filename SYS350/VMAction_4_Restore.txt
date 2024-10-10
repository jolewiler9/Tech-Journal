def restore_latest_snapshot():
    try:
        vm_name = input("Enter the name of the VM to restore the latest snapshot: ")
        vm = find_vm(vm_name)
        snapshot = vm.snapshot
        if snapshot is not None:
            latest_snapshot = snapshot.rootSnapshotList[-1]  # Gets the latest snapshot
            print(f"Restoring latest snapshot for VM: {vm.name}")
            task = latest_snapshot.snapshot.RevertToSnapshot_Task()
            task_result = wait_for_task(task)
            print(f"VM {vm.name} restored to the latest snapshot.")
        else:
            print(f"VM {vm.name} has no snapshots to restore.")
    except Exception as e:
        print(f"Error restoring snapshot for VM: {e}")
