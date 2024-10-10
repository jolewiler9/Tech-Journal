def wait_for_task(task):
    try:
        while task.info.state == vim.TaskInfo.State.running:
            time.sleep(2)
        if task.info.state == vim.TaskInfo.State.success:
            return task.info.result
        else:
            raise task.info.error
    except Exception as e:
        print(f"Task failed: {e}")
