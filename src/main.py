import argparse
import asyncio
import uuid


from datetime import datetime, date
from threading import Thread
from src.api import *

from src.Peer import Peer
from src.network.MessageHandler import MessageHandler


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="ip address of current node", type=str, required=True)
    parser.add_argument("-kp", "--kademlia_port", help="kademlia port number of current node", type=int, required=True)
    parser.add_argument("-mp", "--message_port", help="server port number of current node", type=int, required=True)
    parser.add_argument("-ap", "--api_port", help="api port number of current node", type=int)
    parser.add_argument("-n", "--node", help="ip and port of bootstrap node", nargs=2, default=None)

    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.node is not None:
        peer = Peer(args.ip, args.kademlia_port, args.message_port, (args.node[0], int(args.node[1])))
    else:
        peer = Peer(args.ip, args.kademlia_port, args.message_port)

    t = Thread(target=peer.loop.run_forever, daemon=True)

    t.start()

    #OPTIONAL: If wants to use the frontend
    if args.api_port is not None:
        server_api_t = Thread(target=run_api_server, args=[peer, args.api_port], daemon=True)
        server_api_t.start()

    value = ""

    value = initial_menu(peer, value)
    print(value)
    if value == "2":
        page_menu(peer, value)

    t.join()




def register_the_creators(args, peer):
    if args.node is not None:
        asyncio.run_coroutine_threadsafe(peer.register("amanda", "amanda"), loop=peer.loop)
        asyncio.run_coroutine_threadsafe(peer.register("filipe", "filipe"), loop=peer.loop)
        asyncio.run_coroutine_threadsafe(peer.register("pedro", "pedro"), loop=peer.loop)
        asyncio.run_coroutine_threadsafe(peer.register("victor", "victor"), loop=peer.loop)


def initial_menu(peer, value):
    not_finished = True
    while not_finished:
        value = input("Press 1 to register, 2 to login, 0 to exit:\n")
        if value == "1":
            username = input("Username: ")
            password = input("Password: ")
            asyncio.run_coroutine_threadsafe(peer.register(username, password), loop=peer.loop)
        elif value == "2":
            username = input("Username: ")
            password = input("Password: ")
            if asyncio.run_coroutine_threadsafe(peer.login(username, password), loop=peer.loop).result():
                not_finished = False
                break

        elif value == "0":
            not_finished = False
            break
    return value


def page_menu(peer, value):
    while value != "0":
        value = input("1 to logout, 2 to follow , 3 to unfollow, 4 to write a publication, 5 to see time line,  0 to exit:\n")
        if value == "1":
            peer.logout()
            initial_menu(peer, value)
        elif value == "2":
            followedName = input("Who do want to follow:\n")
            asyncio.run_coroutine_threadsafe(peer.follow(followedName), loop=peer.loop)
        elif value == "3":
            followedName = input("Who do want to unfollow:\n")
            asyncio.run_coroutine_threadsafe(peer.unfollow(followedName), loop=peer.loop)
        elif value == "4":
            text = input("What have you been wondering?\n")
            date_msg = get_pub_date()
            asyncio.run_coroutine_threadsafe(peer.publish(date_msg, text), loop=peer.loop)
        elif value == "5":
            asyncio.run_coroutine_threadsafe(peer.show_timeline({}), loop=peer.loop)

            """
            try:
                showed = {}
                while True:
                    asyncio.run_coroutine_threadsafe(peer.show_timeline(showed), loop=peer.loop)
            except KeyboardInterrupt:
                print('end of time line! bye bye!')
                """


def get_pub_date():
    now = datetime.now()
    today = date.today()
    date_msg = today.strftime("%B %d, %Y") + " - " + now.strftime("%H:%M:%S")
    return date_msg


if __name__ == "__main__":
    main()
