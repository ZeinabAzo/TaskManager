from src.core.models import Task

class Controller:
    def __init__(self, manager):
        self.manager = manager
        self.commands = {
            "INSERTASK": self.add_task,
        }

    def add_task(self, args : list):
        try:
            id : int = int(args[0])
            start_time = int(args[1])
            end_time = int(args[2])
            value = int(args[3])
        except (ValueError, IndexError):
            print(">>> [ERROR]: Invalid arguments for InsertTask.")
            return
        
        self.manager.add_task(id, start_time, end_time, value)
    
    def dispatch(self, cmd: str, args: list) -> None:
        if cmd not in self.commands:
            print(">>> [ERROR]: Command not found.")
            return
        
        self.commands[cmd](args)
        

            