import logging
import asyncio
from typing import Tuple
from kademlia.network import Server


class Node:
    ip: str
    k_port: int
    bootstrap_node: Tuple[str, int] = None
    server = Server()

    def __init__(self, ip: str, k_port: int, bootstrap_node: Tuple[str, int] = None):
        self.ip = ip
        self.k_port = k_port
        self.bootstrap_node = bootstrap_node
        ###self.set_logger()

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.server.listen(self.k_port, self.ip))
        if self.bootstrap_node:
            self.loop.run_until_complete(self.server.bootstrap([self.bootstrap_node]))

    def set_logger(self) -> None:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    def send_message(self, node_ip: str, node_port: str, message: str) -> None:
        asyncio.run_coroutine_threadsafe(send_message(node_ip, node_port, message), loop=self.loop)


async def send_message(node_ip: str, node_port: str, message: str) -> None:
    try:
        _, writer = await asyncio.open_connection(node_ip, node_port)
        writer.write(message.encode())
        writer.write_eof()
        await writer.drain()
        return True
    except Exception as e:
        return False
