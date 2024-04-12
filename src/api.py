from flask import *
from flask_cors import CORS
from src.Peer import Peer
from src.main import get_pub_date
import json
import asyncio

server_api = Flask(__name__)
CORS(server_api)
peer = None

def run_api_server(p, pt):
    global peer 
    peer = p
    server_api.run(port=pt)

@server_api.route('/register', methods=['GET'])
def api_register():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    success = asyncio.run_coroutine_threadsafe(peer.register(username, password), loop=peer.loop).result()
    
    if (success):
        json_dump = json.dumps({"success": True, "message": "User Registered Successfully"})
    else:
        json_dump = json.dumps({"success": False, "message": "User Already Registered"})
    return json_dump

@server_api.route('/login', methods=['GET'])
def api_login():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))
    success = asyncio.run_coroutine_threadsafe(peer.login(username, password), loop=peer.loop).result()
    
    if (success):
        json_dump = json.dumps({"success": True, "message": "User Logged Successfully"})
    else:
        json_dump = json.dumps({"success": False, "message": "Login Error"})
    return json_dump

@server_api.route('/logout', methods=['GET'])
def api_logout():
    peer.logout()
    
    json_dump = json.dumps({"success": True, "message": "Logged Out Successfully"})
    return json_dump

@server_api.route('/follow', methods=['GET'])
def api_follow():
    followUsername = str(request.args.get('followUsername'))
    success = asyncio.run_coroutine_threadsafe(peer.follow(followUsername), loop=peer.loop).result()
    
    if (success):
        json_dump = json.dumps({"success": True, "message": "User Followed Successfully"})
    else:
        json_dump = json.dumps({"success": False, "message": "User Doesn't Exist"})
    return json_dump


@server_api.route('/unfollow', methods=['GET'])
def api_unfollow():
    followUsername = str(request.args.get('followUsername'))
    success = asyncio.run_coroutine_threadsafe(peer.unfollow(followUsername), loop=peer.loop).result()
    
    if (success):
        json_dump = json.dumps({"success": True, "message": "User Unfollowed Successfully"})
    else:
        json_dump = json.dumps({"success": False, "message": "Error to Unfollow"})
    return json_dump

@server_api.route('/get_following', methods=['GET'])
def api_get_following():
    return peer.info["following"]

@server_api.route('/get_followers', methods=['GET'])
def api_get_followers():
    
    user_followed_info_str = asyncio.run_coroutine_threadsafe(peer.server.get(peer.username), loop=peer.loop).result()
    user_followed_info = json.loads(user_followed_info_str)
    return user_followed_info["followers"]

@server_api.route('/publish', methods=['GET'])
def api_publish():
    publishContent = str(request.args.get('publishContent'))
    publishDate = get_pub_date()
    asyncio.run_coroutine_threadsafe(peer.publish(publishDate, publishContent), loop=peer.loop).result()
    
    json_dump = json.dumps({"success": True, "message": "Content Published Successfully"})
    return json_dump

@server_api.route('/posts', methods=['GET'])
def api_posts():
    posts = asyncio.run_coroutine_threadsafe(peer.get_timeline_posts({}), loop=peer.loop).result()
    json_dump = json.dumps(posts)
    return json_dump

    