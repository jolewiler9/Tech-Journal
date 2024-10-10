def delete_vm():
    try:
        vm_name = input("Enter the name of the VM you want to delete: ")
        vm = find_vm(vm_name)
        confirm = input(f"Are you sure you want to delete {vm.name} from disk? This action cannot be undone. (yes/no): ").lower()
        if confirm == 'yes':
            print(f"Deleting VM: {vm.name}")
            task = vm.Destroy_Task()
            task_result = wait_for_task(task)
            print(f"VM {vm.name} has been deleted from disk.")
        else:
            print("VM deletion aborted.")
