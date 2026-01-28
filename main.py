from src.manager import TaskManager
from src.controller import Controller

def start(controller: Controller) -> None:
    while True:
        command = input("> ").strip()

        if not command:
            continue
        if command.lower() == "exit":
            break

        tokens: list = command.split()
        cmd: str = tokens[0]
        args: list = tokens[1:]

        controller.dispatch(cmd, args)

def main():
    task_manager = TaskManager()
    my_controller = Controller(task_manager)
    start(my_controller)

if __name__ == "__main__":
    main()
