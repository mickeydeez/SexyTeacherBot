import threading
import time
import json

from Bot import Bot
from CustomChannels import check_nick
import CustomChannels

art = """
   _____              _______              _               ____        _
  / ____|            |__   __|            | |             |  _ \      | |
 | (___   _____  ___   _| | ___  __ _  ___| |__   ___ _ __| |_) | ___ | |_
  \___ \ / _ \ \/ / | | | |/ _ \/ _` |/ __| '_ \ / _ \ '__|  _ < / _ \| __|
  ____) |  __/>  <| |_| | |  __/ (_| | (__| | | |  __/ |  | |_) | (_) | |_
 |_____/ \___/_/\_\\__, |_|\___|\__,_|\___|_| |_|\___|_|  |____/ \___/ \__|
                    __/ |
                   |___/
                                  Special thanks to ClaudiaD & l33t
"""

CONF_FILENAME = "conf.json"

data = json.load(open(CONF_FILENAME, "r"))
conf = data["conf"]

bot = Bot(data)


def chat():
    while True:
        msg = input()
        bot.message(msg, conf["chans"][0])


def bot_help(chan=None, arg=None):
    if chan in data and "help" in data[chan] and arg in data[chan]["help"]:
        return data[chan]["help"][arg]

    if arg in data["commands"]:
        return "Quick response command. Use: ?%s <nick>" % arg.lower()

    commands = [x for x in data["commands"]]
    if chan in data:
        if "commands" in data[chan]:
            if arg in data[chan]["commands"]:
                return "Quick response command. Use: ?%s <nick>" % arg.lower()
            commands += [x for x in data[chan]["commands"]]

        if "actions" in data[chan]:
            if arg in data[chan]["actions"]:
                return "There is no help for that command. Try: ?%s" % arg.lower()
            commands += [x for x in data[chan]["actions"] if len(x) > 3]
    commands.sort()

    cmds = ", ".join("?%s" % x for x in commands)
    msg = "Available commands: \u0002%s\u000F." % cmds
    return check_nick(msg, arg)


def add_user(user):
    sha2 = bot.sha2(user)
    if sha2 not in data["users"]:
        data["users"].append(sha2)
        write_data(data)
        bot.notice(user, "You have been added to the database.")


def exec_command(obj, void, arg):
    try:
        func = getattr(obj, void)
        response = func(arg) if arg else func()
    except:
        response = "That is not a valid command format."

    return response


def listen_irc():
    info = bot.listen()

    if not info:
        return

    nick, chan, cmd, arg = info
    response = "The command you are trying to execute does not exist."

    if cmd == "help" or cmd == "h":
        response = bot_help(chan, arg)
    elif cmd in data["commands"]:
        response = data["commands"][cmd]
    elif chan in data:
        if cmd in data[chan]["commands"]:
            response = data[chan]["commands"][cmd]
        elif cmd in data[chan]["actions"]:
            void = str(data[chan]["actions"][cmd])
            obj = getattr(CustomChannels, chan.title())(data, bot)
            response = exec_command(obj, void, arg)

    if response:
        bot.message(check_nick(response, arg), chan)


def main():
    print(art)

    bot.auth()
    bot.ping()
    time.sleep(1)
    bot.join()
    threading.Thread(target=chat).start()

    print("[+] Bot is up and running.\n")
    print(conf["chans"][0] + "\n")

    while True:
        listen_irc()

if __name__ == "__main__":
    test()
