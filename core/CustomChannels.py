import json
import random
import re

CONF_FILENAME = "conf.json"
VIDEO_FORMAT = re.compile("^http(?:s?)://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]*)(&(amp;)?‌​[\w\?‌​=]*)?$")


def check_nick(msg, nick=None):
    return "%s: %s" % (nick, msg) if nick else msg


def write_data(data):
    w = open(CONF_FILENAME, "w")
    json.dump(data, w)
    w.close()


class Learninghub(object):
    def __init__(self, data, bot):
        self.data = data
        self.bot = bot
        self.name = "#learninghub"

    def welcome(self, nick):
        greet = (
            "Welcome to #learninghub %s! Here you'll find lots of resources and people to learn hacking/pentesting "
            "as well as other IT subjects. Type ?goldmine to get started and get rid of the welcome message. Type "
            "?desc <course_number> to know the description of a course. You have to use the course number in the "
            "ghostbin. Type ?help for more." % nick
        )
        self.bot.notice(nick, greet)

    def users(self, nick=None):
        num = len(self.data[self.name]["users"])
        msg = "There are %d registered users." % num
        return check_nick(msg, nick)

    def random_course(self, nick=None):
        i = random.choice(self.data[self.name]["courses"])
        msg = "%s. %s." % (i["id"], i["title"])
        return check_nick(msg, nick)

    def desc(self, course):
        try:
            info = self.data[self.name]["courses"][int(course)]
            d = info["desc"]
            return d
        except:
            return "?desc <0-108>"

    def link(self, course):
        try:
            info = self.data[self.name]["courses"][int(course)]
            url = info["link"]
            return url
        except:
            return "?link <0-108>"

    def whatof(self, arg=None):
        if arg in self.data[self.name]["whatof"]:
            return self.data[self.name]["whatof"][arg]
        else:
            return "There is no data for this user."


class Opsec(object):
    def __init__(self, data, bot):
        self.data = data
        self.bot = bot
        self.name = "#opsec"

    def video(self, nick=None):
        videos = self.data[self.name]["videos"]
        return check_nick(random.choice(videos), nick)

    def add_video(self, video=None):
        if video in self.data[self.name]["videos"]:
            return "Video already exists."

        if not VIDEO_FORMAT.match(video):
            return "Wrong video format. Please add youtube links only."

        self.data[self.name]["videos"].append(video)
        write_data(self.data)
        return "Video added successfully."
