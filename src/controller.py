from src.core.task import Task

class Controller:
    def __init__(self, manager):
        self.manager = manager
        self.commands = {
            "InsertTask": self.add_task,
            "DeleteTask" : self.delete_task,
            "UpdateTask": self.update_task,
            "QueryTaskId": self.search,
        }

    def add_task(self, args : list):
        if len(args) != 4 :
            print(">>> [ERROR]:  Invalid arguments for InsertTask.")
            return
        
        try:
            id = int(args[0])
            start_time = int(args[1])
            end_time = int(args[2])
            value = int(args[3])
        except (ValueError):
            print(">>> [ERROR]: Invalid arguments for InsertTask.(Arguments are not integer)")
            return
        
        self.manager.add_task(id, start_time, end_time, value)

    def delete_task(self, args: list):
        if len(args) != 1:
            print(">>> [ERROR]:  Invalid arguments for InsertTask.")
            return
        
        try:
            id = int(args[0])
        except (ValueError):
            print(">>> [ERROR]: Invalid arguments for InsertTask.(Arguments are not integer)")
            return
        
        self.manager.remove_task(id)
    
    def update_task(self, args: list):
        if len(args) != 4 :
            print(">>> [ERROR]:  Invalid arguments for InsertTask.")
            return
        
        try:
            id = int(args[0])
            start_time = int(args[1])
            end_time = int(args[2])
            value = int(args[3])
        except (ValueError):
            print(">>> [ERROR]: Invalid arguments for InsertTask.(Arguments are not integer)")
            return
        
        self.manager.update_task(id, start_time, end_time, value)
    
    def search(self, id: int):
        task : Task = self.manager.get_task_id(id)
        if task:
            print(f"Task info ->  time: ({task.start_time}, {task.end_time}), id:{task.id}, value: {task.value}")
        else:
            print("Task not found")

        return
        
    
    def dispatch(self, cmd: str, args: list) -> None:
        if cmd not in self.commands:
            print(">>> [ERROR]: Command not found.")
            return
        
        self.commands[cmd](args)
        

            