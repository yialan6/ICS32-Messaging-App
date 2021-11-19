#Alan Yi
#yia6@uci.edu
#29003386

import socket
from collections import namedtuple
import json



DSConnect = namedtuple('DSConnect', ['socket', 'send', 'recv'])
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def init(sck):
  """Initializes tuple for connection details."""
  try:
      f_send = sck.makefile('w')
      f_recv = sck.makefile('r')
  except:
      raise SocketConnectionError("Enter a valid socket connection.")
      
  return DSConnect(
      socket = sck,
      send = f_send,
      recv = f_recv
  )



def messenger(ds_connect: DSConnect, token: str, entry: str, recipient: str):
  """Connects to server via dsuserver IP."""

  token = '"{}"'.format(token)
  entry = '"{}"'.format(entry)
  recipient = '"{}"'.format(recipient)
  directmsg = '{"token":' + token + ', "directmessage": {"entry": ' + entry + ',"recipient":' + recipient + ', "timestamp": "1603167689.3928561"}}'
  write(ds_connect, directmsg) #Sends connection details to socket.
  received = read(ds_connect)
  received = extract_json1(received, 'send')
  
  return received


def unread_msg(ds_connect: DSConnect, token: str):
  token = '"{}"'.format(token)
  json_msg = '{"token":' + token + ', "directmessage": "new"}'
  write(ds_connect, json_msg) #Sends connection details to socket.
  received = read(ds_connect)
  received = extract_json1(received, 'receive')
  
  return received


def all(ds_connect: DSConnect, token: str):
  # Request all messages from the DS server
  allmsg = '{{"token":"{}", "directmessage": "all"}}'.format(token)
  write(ds_connect, allmsg) #Sends connection details to socket.
  received = read(ds_connect)
  extract = extract_json1(received, 'receive')
  return extract


def join(ds_connect: DSConnect, username: str, password: str):
  """Connects to server via dsuserver IP."""

  username = '"{}"'.format(username)
  password = '"{}"'.format(password)
  profile = '{"join": {"username": ' + username + ',"password": ' + password + ',"token":"user_token"}}'
  write(ds_connect, profile) #Sends connection details to socket.
  received = read(ds_connect) 
  return received


def write(ds_connect: DSConnect, data: str):
  """Writes into socket file."""

  ds_connect.send.write(data + '\n')
  ds_connect.send.flush()


def read(ds_connect: DSConnect):
  """Reads from socket file."""

  received = ds_connect.recv.readline()[:-1]
  return received


def disconnect(ds_connect: DSConnect):
  """Disconnect from socket connection."""

  ds_connect.send.close()
  ds_connect.recv.close()


def extract_json(json_msg:str) -> DataTuple:
  """Extract message received from server."""

  try:
      json_obj = json.loads(json_msg)
      validity = json_obj['response']['type']
      message = json_obj['response']['message']
      if validity == 'ok':
          token = json_obj['response']['token']
      elif validity == 'error':
          print('Could not successfully connect to server.')
  except json.JSONDecodeError:
      print("Json cannot be decoded.")

  return DataTuple(validity, message, token)


def extract_json1(json_msg:str, state) -> DataTuple:
  """Extract message received from server."""

  try:
      json_obj = json.loads(json_msg)
      if state == 'send':
          validity = json_obj['response']['type']
      elif state == 'receive':
          validity = json_obj['response']['messages']
      return validity
  except json.JSONDecodeError:
      print("Json cannot be decoded.")
      
