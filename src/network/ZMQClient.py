import zmq

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 1


class ZMQClient:

    def __init__(self, host, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.server_url = "tcp://{0}:{1}".format(host, port)
        print("client: ", self.server_url)
        self.socket.connect(self.server_url)

    def send_msg(self, msg):
        self.socket.send_multipart(msg)
        print("Sending ", msg)
        retries_left = REQUEST_RETRIES
        while True:
            if (self.socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
                resp = self.socket.recv()
                print("Received: \"%s\"" % resp)
                return resp
            retries_left -= 1
            print("No response from server")
            # Socket is confused. Close and remove it.
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()
            if retries_left <= 0:
                return b"ERROR: Server seems to be offline, abandoning"

            print("Reconnecting to server…")
            # Create new connection
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect(self.server_url)
            print("Resending ", msg)
            self.socket.send_multipart(msg)

    def close(self):
        self.socket.close()
        self.context.term()
