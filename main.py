import json
import time
import requests
import websocket

status = "dnd"  # online/dnd/idle

GUILD_ID = ADD_YOUR_SERVER_ID_HERE
CHANNEL_ID = ADD_YOUR_CHANNEL_ID_HERE
SELF_MUTE = True
SELF_DEAF = False

def validate_token(token, headers):
  validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
  if validate.status_code != 200:
    print(f"[ERROR] Token '{token}' might be invalid. Please check it again.")
    return False
  return True

def get_user_info(token, headers):
  userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
  return userinfo["username"], userinfo["id"]

def joiner(token, status):
  ws = websocket.WebSocket()
  ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
  start = json.loads(ws.recv())
  heartbeat = start['d']['heartbeat_interval']
  auth = {
      "op": 2,
      "d": {
          "token": token,
          "properties": {"$os": "Windows 10", "$browser": "Google Chrome", "$device": "Windows"},
          "presence": {"status": status, "afk": False}
      },
      "s": None,
      "t": None
  }
  vc = {
      "op": 4,
      "d": {"guild_id": GUILD_ID, "channel_id": CHANNEL_ID, "self_mute": SELF_MUTE, "self_deaf": SELF_DEAF}
  }
  ws.send(json.dumps(auth))
  ws.send(json.dumps(vc))
  time.sleep(heartbeat / 1000)
  ws.send(json.dumps({"op": 1, "d": None}))

def run_joiner(tokens):
  for token in tokens:
    headers = {"Authorization": token, "Content-Type": "application/json"}
    if not validate_token(token, headers):
      continue  # Skip to the next token if validation fails
    username, userid = get_user_info(token, headers)
    print(f"Logged in as {username} ({userid}).")
    joiner(token, status)
    print("-" * 50)  # separator between users
    time.sleep(3)  # delay between joining for each token

# Add your tokens here (replace "token1", "token2" and so on with your actual tokens)
tokens = ["token1", "token2", "token3 and so on"]

keep_alive()
run_joiner(tokens)
