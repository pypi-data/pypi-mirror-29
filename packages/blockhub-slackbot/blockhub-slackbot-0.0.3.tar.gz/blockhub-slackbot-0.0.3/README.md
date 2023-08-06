# slackbot
a framework for easily creating python based slackbots

simply

```sh
pip install slackbot
```

and then 

```python
from slackbot import Bot
from slackbot.
...
class MyBot(Bot)
  
  class add_to_agenda:
      def __init__(self):
          self.desc = "add something to the agenda"
          self.allowed_commands = ['date', 'something']
      def __cal__(self, args)
      # this is what actually gets executed
          a = do_something()
          return a, True (or False)
```

Each call needs to return a tuple, where the first is either a formatted attachment, and the second indicates if it is a proper slack attachment (True) or just a string.

Need to perform regular tasks? Simply name your subclass on_cycle_something, and make sure you initialize it with a frequency

```python
class MyBot(Bot)
  
  class on_cycle_check_agenda:
      def __init__(self):
          self.frequency = 30000
          self.allowed_commands = ['date', 'something']
      
      def __cal__(self, args)
      # this is what actually gets executed
          a = do_something()
          return a, True (or False)
```

Cycle length is determined by delay, standard it set at 0.2s

on_cycle does not need to implement desc or allowed_commands, as it cannot be called from slack.

The names of the commands correspond with the class name. In this example, saying 
```
@mybot add_to_agenda date title
```

Will call

```python
MyBot.add_to_agenda([date, title])
```