import hashlib
import socket
import ssl
import re

__author__ = "Anonymous"
__license__ = "GPLv3"


class Bot(object):
    def __init__(self, data):
        self.data = data
        self.conf = data["conf"]
        self.s = None
        self.connect()

    @staticmethod
    def sha2(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
            self.s.setblocking(1)
            self.s = ssl.wrap_socket(self.s)
            self.s.connect((self.conf["irc"], self.conf["port"]))
        except Exception as e:
            print("Failed to connect. %s:%d" % (self.conf["irc"], self.conf["port"]))
            print(e)
            exit()

    def _send(self, msg):
        self.s.send(msg.encode("UTF-8"))

    def message(self, msg, chan):
        self._send("PRIVMSG %s :%s\r\n" % (chan, msg))

    def notice(self, user, msg):
        self._send("NOTICE %s :%s\r\n" % (user, msg))

    def auth(self):
        print("[+] Sending credentials for %s" % self.conf["nick"])
        if self.conf["pass"]:
            self._send("PASS %s\r\n" % self.conf["pass"])
        self._send("NICK %s\r\n" % self.conf["nick"])
        self._send("USER %s 0 * :%s\r\n" % (self.conf["user"], self.conf["real"]))
        print("[+] Credentials sent. Waiting for authentication.")

    def ping(self):
        while True:
            try:
                recvd = self.s.recv(4096).decode()

                if "PING" in recvd:
                    self.pong(recvd)
                elif "%s!%s" % (self.conf["nick"], self.conf["user"]) in recvd:
                    print("[+] Ping completed")
                    break

            except socket.timeout:
                raise("[-] Error: ", socket.timeout)

    def pong(self, msg):
        num = msg.strip("PING :")
        self._send("PONG :%s" % num)

    def login(self):
        self._send(":source PRIVMSG nickserv :identify %s\r\n" % self.conf["pass"])

    def join(self):
        print("[+] Joining channels.\n")

        # Ensure the login is made correctly.
        # Most times the first login doesn't connect.
        [self.login() for _ in range(3)]

        for x in self.conf["chans"]:
            self._send("JOIN %s\r\n" % x)

        self._send("MODE %s +B\r\n" % self.conf["nick"])

    def listen(self):
        valid = re.compile(r"^:(?P<nick>[\w-]+)!\S* (?P<mode>\w+) :?(?P<chan>#?\w+)(\s:\?(?P<cmd>\w+)(\s(?P<arg>\w+))?)?")

        try:
            recvd = self.s.recv(4096).decode()
            data = valid.match(recvd)

            if "PING" == recvd[:4]:
                self.pong(recvd)
                return
            elif not data:
                return

            nick = data.group("nick")
            mode = data.group("mode")
            chan = data.group("chan")
            cmd = data.group("cmd")
            arg = data.group("arg")

            # Allow the bot to have private conversations
            if chan == self.conf["nick"]:
                chan = nick
            elif chan:
                chan = chan.lower()

            # Send welcome message to new users
            if mode == "JOIN" and self.sha2(nick) not in self.data["users"]:
                cmd = "welcome"

            if arg:
                print("<%s:%s> %s %s" % (nick, chan, cmd, arg))
            else:
                print("<%s:%s> %s" % (nick, chan, cmd))

            if isinstance(cmd, str):
                return nick, chan, cmd, arg
        except socket.timeout:
            print("[-] Error: Socket timeout.")
            self.listen()
        except Exception as e:
            self.s.close()
            raise e
