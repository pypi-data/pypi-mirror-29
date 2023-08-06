
AsyncBots
==========

This library provides a simple ``asyncio`` based interface for writing ``RTM <https://api.slack.com/rtm>`` bots for Slack. Many distinct functions can be run through a single Slack bot plugin, triggered by user defined commands (e.g. ``!myCommand``).

Example
```````
A bot which can be triggered by the message ``!greet Guido`` looks like this:

.. code:: python

    from asyncbots.bot import SlackBot, register
    from asyncbots.command import MessageCommand
    from pyparsing import alphas, Word

    class MyBot(SlackBot)
        def __init__(self):
            self.name = 'My Bot'

            # Match 'greet' followed by any word
            self.expr = 'greet' + Word(alphas).setResultsName('user')

        @register()
        async def handler(self, sender, channel, parsed_message):
            return MessageCommand('Hello ' + parsed_message['user'])


