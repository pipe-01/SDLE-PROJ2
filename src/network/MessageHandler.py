import asyncio
import json
import pickle

from src.network.Message import Message, Command
from src.network.ZMQServer import ZMQServer

REQUEST_TIMEOUT = 2500

msgs_file_path = "data/{0}_messages.pickle"


class MessageHandler:

    def __init__(self, username, port):
        print("init msg handle", username)
        self.username = username
        self.port = port
        self.loop = asyncio.get_event_loop()
        # self.loop.run_until_complete(self.server())
        # self.server()

    # self.loop = asyncio.get_event_loop()
    # self.loop.run_until_complete(self.server.listen(self.port, self.ip))

    async def server(self):
        s1 = ZMQServer(self.port)
        await s1.receive(self.msgProcess)

    def msgProcess(self, msgList):
        print("msgProcess", msgList)
        msg = Message.listToMessage(msgList)

        if Command.PUT == msg.cmd:
            return self.processPut(msg)
        elif msg.cmd == Command.GET:
            return self.processGet(msg)

    def processGet(self, msg):
        print("GET")
        username = msg.username
        try:
            msg_file = open(msgs_file_path.format(self.username), "rb")
            all_messages = pickle.load(msg_file)
            if username not in all_messages:
                return b"[]"
            else:
                messages = all_messages[username]
            return bytes(str(messages), "utf-8")
        except FileNotFoundError:
            return b"ERROR: user not found"

    def processPut(self, msg):
        print("PUT")
        sender_username = msg.username
        value = msg.value
        try:
            msg_file = open(msgs_file_path.format(self.username), "rb")
            messages = pickle.load(msg_file)
        except FileNotFoundError:
            messages = {}

        if sender_username not in messages:
            messages[sender_username] = [value]
        else:
            messages[sender_username].append(value)
        filename = msgs_file_path.format(self.username)
        with open(filename, 'wb+') as file:
            pickle.dump(messages, file)
        print(messages)

        return b"SUCESS: put"

    def write_pickle(filename, data):
        print(filename)
        with open(filename, 'wb+') as file:
            pickle.dump(data, file)

    def stringToBytes(msg):
        return bytes(str(msg), "utf-8")

    def bytesToString(bmsg):
        return bmsg.decode("utf-8")

# async def main_thread(port):
#     await asyncio.gather(Server(port))

# async def main_thread(self):
#     self.loop.run_until_complete(await asyncio.gather(self.server()))
