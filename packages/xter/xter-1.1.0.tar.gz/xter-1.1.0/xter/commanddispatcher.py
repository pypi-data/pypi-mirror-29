from xter.commandlistener import CommandListener


class CommandDispatcher:
    def __init__(self):
        self.listeners = []

    def dispatch_command(self, command, task_parameters):
        for listener in self.listeners:
            if isinstance(listener, CommandListener):
                if command.name in listener.for_commands:
                    status = listener.execute(command, task_parameters)
                    if not isinstance(status, (int, long)) or status > 2:
                        raise ValueError('Your Listener needs to return an integer 1=success, 2=fail')
                    if status > 1:
                        return status
            else:
                return 2
        return 1

    def add_listener(self, listener):
        self.listeners.append(listener)
