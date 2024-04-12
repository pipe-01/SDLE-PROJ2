import asyncio
from datetime import datetime, timedelta
import os
import pickle

from src.Node import Node
from typing import Tuple
import bcrypt
import json
import uuid

from src.Database import Database
from src.network import client
from threading import Lock
from src.network.MessageHandler import MessageHandler

# MENSSAGE_FILE_PATH = os.path.join("C:\\Users\\mika1\\Desktop\\Filipe\\proj2\\data", "{0}_messages.pickle")
MENSSAGE_FILE_PATH = os.path.join("data", "{0}_messages.pickle")


# lock_follow = Lock()
# lock_unfollow = Lock()


class Peer(Node):

    def __init__(self, ip: str, k_port: int, m_port: int, bootstrap_node: Tuple[str, int] = None):
        super().__init__(ip, k_port, bootstrap_node)
        self.database = None
        self.info = None
        self.username = None
        self.m_port = m_port

    def __int__(self, ip, k_port, m_port, bootstrap_node: Tuple[str, int] = None):
        super().__int__(ip, k_port, m_port, bootstrap_node)

    async def register(self, username, password):
        user_info = await self.server.get(username)
        if user_info is None:
            self.username = username
            self.info = {
                "ip": self.ip,
                "k_port": self.k_port,
                "m_port": self.m_port,
                "following": [],
                "followers": [],
            }
            await self.server.set(self.username, json.dumps(self.info))
            pwd_hash = self.hash_password(password)
            self.initiate_database(self.ip, self.k_port)
            try:
                self.database.insert(username, pwd_hash)
            except Exception as ex:
                print(ex)
            print("User registered with success!\n")
            return True
        else:
            print("User already registered\n")
            '''
            self.info = {
                "ip": self.ip,
                "k_port": self.k_port,
                "m_port": self.m_port,
                "following": user_info["following"],
                "followers": user_info["followers"],
            }
            '''
            return False

    async def login(self, username, password):

        print("\nTrying to login...")
        self.initiate_database(self.ip, self.k_port)
        user = self.database.search(username)
        user_info = await self.update_info(username)
        if user_info is None:
            print("User not registered\n")
            return False
        pwd_bytes = password.encode("utf-8")
        if bcrypt.checkpw(pwd_bytes, user[0]):
            print("Logged with success!\n")
            await self.update_following_msgs()
            msg_handler = MessageHandler(username, self.m_port)
            asyncio.run_coroutine_threadsafe(msg_handler.server(), loop=msg_handler.loop)
            return True
        print("Passwords don't match\n")
        return False

    async def update_info(self, username):
        user_info = await self.server.get(username)
        if user_info is None:
            return None
        print(user_info)
        self.username = username
        self.info = json.loads(user_info)
        self.info["ip"] = self.ip
        self.info["k_port"] = self.k_port
        return user_info

    def logout(self):
        # self.server.stop()
        # self.loop.stop()
        print("User {0} Logged out!".format(self.username))

    def hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt)

    def initiate_database(self, ip, k_port):
        print("initiate_database")
        self.database = Database(ip, k_port)

    async def follow(self, followedName):
        print("\nTrying to follow...")
        # lock_follow.acquire()
        await self.update_info(self.username)
        print(self.info["following"])
        if followedName in self.info["following"]:
            print("You already folllow the user {0}".format(followedName))
        else:
            user_followed_info_str = await self.server.get(followedName)
            print(user_followed_info_str)
            if user_followed_info_str is None:
                print("User {0} does not exists".format(followedName))
                return False
            user_followed_info = json.loads(user_followed_info_str)
            self.info["following"].append(followedName)
            print(self.info["following"])
            user_followed_info["followers"].append(self.username)

            await self.server.set(self.username, json.dumps(self.info))
            await self.server.set(followedName, json.dumps(user_followed_info))

            print(await self.server.get(self.username))
            print(await self.server.get(followedName))

            await self.update_following_msgs()
        # lock_follow.release()
        return True

    async def unfollow(self, followedName):
        print("\nTrying to unfollow...")
        await self.update_info(self.username)
        if followedName in self.info["following"]:
            # lock_unfollow.acquire()
            print(followedName)
            user_followed_info_str = await self.server.get(followedName)
            print(user_followed_info_str)
            if user_followed_info_str is None:
                print("User {0} does not exists".format(followedName))
                return False
            user_followed_info = json.loads(user_followed_info_str)
            print(user_followed_info)
            self.info["following"].remove(followedName)
            print(self.info)
            user_followed_info["followers"].remove(self.username)
            print(user_followed_info)
            await self.server.set(self.username, json.dumps(self.info))
            print("1 set")
            await self.server.set(followedName, json.dumps(user_followed_info))
            print("2 set")
            # lock_unfollow.release()
        else:
            print("You don't follow the User {0}".format(followedName))
            return False
        return True

    async def publish(self, date_msg, text):
        await self.update_info(self.username)
        msg_id = str(uuid.uuid4().hex) + self.username
        msg = str((msg_id, self.username, text, date_msg))
        print(msg)
        for follower_name in self.info["followers"]:
            print(follower_name)
            follower_info = json.loads(await self.server.get(follower_name))
            print(follower_info)
            follower_messages_port = follower_info["m_port"]
            print(follower_messages_port)
            follower_messages_ip = follower_info["ip"]
            print(follower_messages_ip)
            client.put(follower_messages_ip, follower_messages_port, self.username, msg)

        self.update_messages(self.username, [bytes(str(msg), "utf-8")])  # precisa ser uma lista

    def update_messages(self, publisher_name, msgs):
        msgs_file_path = MENSSAGE_FILE_PATH.format(self.username)
        try:
            msg_file = open(msgs_file_path, "rb")
            messages = pickle.load(msg_file)
            msg_file.close()
        except FileNotFoundError:
            messages = {}

        if publisher_name not in messages:
            messages[publisher_name] = msgs
        else:
            messages[publisher_name].extend(msgs)
        filename = msgs_file_path

        with open(filename, 'wb+') as file:
            pickle.dump(messages, file)
            file.close()
        print("update msgs final", messages)

    def expiredDate(self, msg):
        (_, _, _, str_date) = eval(msg.decode('utf-8'))
        datetime_object = datetime.strptime(str_date, '%B %d, %Y - %H:%M:%S')
        return datetime_object + timedelta(days=1) < datetime.now()

    def dateFilter(self, msg):
        (_, _, _, date) = msg
        return self.expiredDate(date)

    def garbage_collector(self, dict_msgs):
        for name in dict_msgs:
            if name != self.username:
                listMsg = dict_msgs[name]
                dict_msgs[name] = [msg for msg in listMsg if not self.expiredDate(msg)]
        return dict_msgs

    async def update_following_msgs(self):
        await self.update_info(self.username)
        for following_name in self.info["following"]:
            msgs_following = await self.get_msgs(following_name)
            self.update_messages(following_name, msgs_following)

    async def get_msgs(self, following_name):
        following_info = json.loads(await self.server.get(following_name))
        following_messages_port = following_info["m_port"]
        following_messages_ip = following_info["ip"]
        result = client.get(following_messages_ip, following_messages_port, following_name)
        if not result.startswith(b"ERROR:"):  # offline
            return eval(result.decode("utf-8"))
        else:
            for follower in following_info["followers"]:
                if follower != self.username:
                    follower_info = json.loads(await self.server.get(follower))
                    result = client.get(follower_info["ip"], follower_info["m_port"], following_name)
                    if not result.startswith(b"ERROR:"):  # found some follower online
                        return eval(result.decode("utf-8"))
        print("update of {0} failed", following_name)
        return []

    async def read_msg_file(self):
        print("read_msg_file begin")
        msgs_file_path = MENSSAGE_FILE_PATH.format(self.username)
        try:
            client_self_msg_file = open(msgs_file_path, 'rb')
            client_self_msg = pickle.load(client_self_msg_file)
            client_self_msg_file.close()
            client_self_msg = self.garbage_collector(client_self_msg)
            client_self_msg_file = open(msgs_file_path, 'wb+')
            pickle.dump(client_self_msg, client_self_msg_file)
        except FileNotFoundError:
            print("file not found: ", msgs_file_path)
            client_self_msg_file = open(msgs_file_path, 'wb+')
            pickle.dump({}, client_self_msg_file)
            client_self_msg = {}
        client_self_msg_file.close()
        return client_self_msg

    ## msgs = { username: [(msg_id, username,  text, date)]
    async def sort_msgs(self, msgs):
        all_msgs = []
        for list_msgs in msgs.values():
            list_msgs = [eval(x.decode('utf-8')) for x in list_msgs]
            all_msgs.extend(list_msgs)
            all_msgs = sorted(all_msgs, key=lambda x: x[3], reverse=True)

        return all_msgs

    async def show_timeline(self, dict_already_showed):
        # print(client_self_msg)
        msgs = await self.read_msg_file()
        ####                   0        1        2      3
        ### sorted_msgs = [((msg_id, username,  text, date))]
        sorted_msgs_by_date = await self.sort_msgs(msgs)

        for msg in sorted_msgs_by_date:
            if msg[0] not in dict_already_showed:
                dict_already_showed[msg[0]] = True
                name = msg[1]
                text = msg[2]
                date = msg[3]
                print("{0}: {1} - {2}".format(name, text, date))

    async def get_timeline_posts(self, dict_already_showed):
        # print(client_self_msg)
        msgs = await self.read_msg_file()
        ####                   0        1        2      3
        ### sorted_msgs = [((msg_id, username,  text, date))]
        sorted_msgs_by_date = await self.sort_msgs(msgs)

        messages = []
        for msg in sorted_msgs_by_date:
            if msg[0] not in dict_already_showed:
                dict_already_showed[msg[0]] = True
                name = msg[1]
                text = msg[2]
                date = msg[3]
                # print("{0}: {1} - {2}".format(name, text, date))
                messages.append({"username": name, "time": date, "content": text})
        return messages
