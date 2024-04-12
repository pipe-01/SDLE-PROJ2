from src.network.Message import Message, Command
from src.network.ZMQClient import ZMQClient


def client(c1, msg):
    return c1.send_msg(msg)


def put(host, port, username, value):  # username de quem escreveu as msgs
    # print("put: " + value)
    return client(ZMQClient(host, port), Message(Command.PUT, username, bytes(value, "utf-8")).toMultipart())


def get(host, port, username):  # username de quem eu quero as msgs
    # print("get: ", host, port, username)
    return client(ZMQClient(host, port), Message(Command.GET, username, b"").toMultipart())
