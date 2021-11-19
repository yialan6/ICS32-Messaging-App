import ds_protocol as prtc
import socket 


class LoginDetailException(Exception):
  """Custom exception for non string type login details."""
  pass


class ServerResponses:
  """Class to hold all recent responses from the server to be
  used by the Messenger App"""
  def __init__(self):
    self.bool = None
    self.all = []
    self.new = []


class DirectMessage:
  """
  Creates a class for message objects. Contains attributes for recipient name, message, and timestamp.
  """
  def __init__(self, recipient=None, message=None, timestamp=None):
    self.recipient = recipient
    self.message = message
    self.timestamp = None



class DirectMessenger:
  """
  Creates a class for messaging functions. Contains attributes for sending messages, retrieving new messages, and retrieving all messages.
  """
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.ds_conn = None
    self.username = username
    self.password = password
    self.dsuserver = dsuserver
    self.responses = ServerResponses()

    if type(self.username) != str or type(self.password) != str or type(self.dsuserver) != str:
      raise LoginDetailException('DirectMessenger class takes strings as arguments.')


  def connect(self):
    """Connects to the dsuserver and extracts user token."""
    try:
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a socket.
      client.connect((self.dsuserver, 2021))

      self.ds_conn = prtc.init(client) #Initializes named tuple attribute containing the socket, sendfile and recvfile.
      json_msg = prtc.join(self.ds_conn, self.username, self.password) #Retrieves json message after joining dsuserver.
      extracted_msg = prtc.extract_json(json_msg) #Decodes json msg from server.
      self.token = extracted_msg.token
    except socket.gaierror:
      raise Exception('Invalid Server Address') from None
    except UnboundLocalError:
      raise Exception('Invalid username/password combo. Username may already be taken.') from None
    except OSError:
      raise Exception('Invalid Server Address') from None

  def send(self, message, recipient) -> bool:
    """Sends a direct message and returns a bool value based on whether the message was successfully sent."""
    if type(message) != str or type(recipient) != str:
      raise LoginDetailException('Message and recipient must be of string type.')
        
    self.connect()
    x = prtc.messenger(self.ds_conn, self.token, message, recipient) #Sends a message to specified recipient.
    prtc.disconnect(self.ds_conn)
    if x == 'ok': #Checks if message was sent successfully.
      self.responses.bool = True
      return True
    else:
      self.responses.bool = False
      return False
  
  

  def retrieve_new(self):
    """Retrieves all unread messages in a list containing the senders' usernames and their messages."""
    self.connect()
    x = prtc.unread_msg(self.ds_conn, self.token) #Initializes list of unread messages.
    prtc.disconnect(self.ds_conn)

    for msg in x: #Iterates through list of unread messages and creates a DirectMessage object for each one.
      message = DirectMessage(msg['from'], msg['message'], msg['timestamp'])
      self.responses.new.append(message)
    return self.responses.new #Returns a list of DirectMessage objects.


  def retrieve_all(self):
    """Retrieves all messages in a list containing the senders' username and their messages."""
    self.connect()
    x = prtc.all(self.ds_conn, self.token)
    prtc.disconnect(self.ds_conn)

    for msg in x: #Iterates through list of all messages and creates a DirectMessage object for each one.
      message = DirectMessage(msg['from'], msg['message'], msg['timestamp'])
      self.responses.all.append(message)
    return self.responses.all #Returns a list of DirectMessage objects.



