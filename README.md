# SexyTeacherBot

The code must be run with python 3.6

SexyTeacherBot is an interactive bot used in educational irc channels.
The main purpose of this bot is to write an easy to use interface as well a providing some dynamic, helpful and fun functionality.

Every channel the bot serves on needs to have a specific tag in the conf.json. That helps the bot coordinate it's commands and functionality. Adding special actions for a certain channel, that is, making it do something other than just provide a "quick response", will require an object under CustomChannels.py. 


For security purposes, conf.json is incomplete. Lacking both 'users' - #learninghub and 'conf'.

```
'users' should contain a list of SHA2 Hashes of registered channel nicks (nicks that have been in the channel before).

'conf' = {
    "irc": str(),       # IRC's address
    "port": int(),      # IRC's port
    "nick": str(),      # Bot's nick name
    "user": str(),      # Bot's user name
    "real": str(),      # Bot's real name
    "pass": str()       # Bot's password
    "chans": [str()],   # Channels bot should connect to, it will only answer in the first one
}
```
