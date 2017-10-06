import json

conf = {
    "conf": "conf.json",
    "users": "users.txt"
}

data = json.load(open(conf["conf"], "r"))


def read_users(filename):
    file = open(filename, "r")
    info = [a for a in file.read().splitlines()]
    file.close()
    return info


data["users"] = read_users(conf["users"])
data["conf"] = {
    "pass": "123654",
    "user": "G3nn1",
    "real": "SexyTeacherBot",
    "chans": [
        "#learninghub",
        "#bots"
    ],
    "irc": "irc.anonops.com",
    "nick": "SexyTeacherBot",
    "port": 6697
}

output = open(conf["conf"], "w")

json.dump(data, output)
