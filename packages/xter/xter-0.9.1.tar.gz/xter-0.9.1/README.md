# XTER

### python 2.7 app
client for the commander api



1. Create A Listener Class
```python

class ExampleListener(CommandListener):
    #the name of the command to listen to
    for_commands = ['Task Number One']

    def execute(self,command):
        for parameter in command.parameters:
            #the parameters from the commands
            pprint(parameter['key'])
            pprint(parameter['value'])
```

2. Create a EventDispatcher and add your listener
```python
dispatcher = CommandDispatcher()
dispatcher.addListener(ExampleListener())
```

3. Create the Commander attach the eventdispatcher and run it
```python
commander = Commander(dispatcher)
commander.run()
```



