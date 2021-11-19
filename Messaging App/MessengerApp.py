
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog

import ds_messenger as ds



"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.users = [] #List to store users currently shwon in treeview.
        self.recipient = None #Recipient that is currently being interacted with.
        self.new = [] #List of unread messages.

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
        
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        self.recipient = self.users[index] #Assigns recipient's name to attribute when clicked on treeview.
        self.reset_ui()
        self.new_message() #Displays new messages.
    

    def new_message(self):
        #check self.new
        templist = self.new.copy()
        for msg in templist: #Checks if user has any new messages stored in self.new attribute list.
            if msg.recipient == self.recipient: #If message recipient matches the clicked node, it displays the new messages and removes the message from self.msg attribute.
                self.set_text_entry(msg.message, 'receive')
                self.new.remove(msg) 
                

        dm = ds.DirectMessenger("168.235.86.101", 'test', 'test') 
        directmsg_list = dm.retrieve_new() #Retrieves all new messages from server.
        for msg in directmsg_list: #Prints new messages if recipient matches selected node. Else, it appends the message into self.new attribute.
            if msg.recipient == self.recipient:
                self.set_text_entry(msg.message, 'receive')
            elif msg.recipient != self.recipient:
                self.new.append(msg)
            self.root
            
        


    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    
    def set_text_entry(self, text:str, state:str=None):
        self.display_frame.config(state=tk.NORMAL) #Enables editing of message display box.
        #Checks if user is sending or recieving.
        if state == 'send':
            x = ds.DirectMessenger("168.235.86.101", 'test', 'test')
            text = x.username + ': ' + text

            if self.display_frame.compare("end-1c", "==", "1.0"): #Checks if text widget is empty.
                self.display_frame.insert('end', text) #Inserts new text into the display box.
            else:
                self.display_frame.insert('end', '\n' + text) #Inserts new text with a newline into the display box.
            self.display_frame.tag_add('background', '0.0', 'end')
            self.display_frame.tag_configure('background', background='lightgreen') #Highlights all messages in green after sending.
            

        elif state == 'receive':
            text = self.recipient + ': ' + text
            if self.display_frame.compare("end-1c", "==", "1.0"): #Checks if text widget is empty.
                self.display_frame.insert('end', text) #Inserts new text into the display box.
            else:
                self.display_frame.insert('end', '\n' + text) #Inserts new text into the display box.
            self.display_frame.tag_add('background', '0.0', 'end')
            self.display_frame.tag_configure('background', background='lightblue')#Highlights all messages in blue after user recieves. 
        
        else: 
            self.display_frame.delete(0.0, 'end') #Deletes all text if another user is clicked on. 
        
        self.display_frame.config(state=tk.DISABLED) #Disables editing of display box.
        self.root.update()


    """
    Inserts a recipient name to the post_tree widget.
    """
    def insert_user(self, recipient):
        self.users.append(recipient)
        self._insert_post_tree(len(self.users), recipient)
        

    """
    Resets all UI widgets to their default state.
    """
    def reset_ui(self):
        self.set_text_entry("")

        self.root.update()


    def _insert_post_tree(self, id, recipient):
        """Enters recipient name into post tree."""     
        self.posts_tree.insert('', id, id, text = recipient)
        
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        #Creates a frame for post_tree.
        posts_frame = tk.Frame(master=self)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        #Creates parent frame for message display box.
        message_frame = tk.Frame(master=self, bg="")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=5, padx=5, ipady=100)
        #Creates message display box.
        self.display_frame = tk.Text(master=message_frame, bg="lightgrey")
        self.display_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.display_frame.config(state=tk.DISABLED) #Disables editing of displaay box.

        #Creates parent frame for send message box.
        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=5, pady=5)
        #Creates frame for send message box.
        entry_editor = tk.Frame(master=entry_frame, bg="red")
        entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        #Prevents the entry_editor from expanding from the internal padding of self.display_frame.
        entry_editor.propagate(0)

        #Creates a frame for the scrollbar.
        scroll_frame = tk.Frame(master=self.display_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        #Creates a text widget.
        self.entry_editor = tk.Text(entry_editor, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, padx=0, pady=0)

        #Creates a scrollbar widget.
        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False, padx=0, pady=0)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, user_callback=None, refresh_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._user_callback = user_callback
        self.refresh_callback = refresh_callback
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()


    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    
    def new_user(self):
        if self._user_callback is not None:
            self._user_callback()
       
        
    def refresh_msg(self):
        if self.refresh_callback is not None:
            self.refresh_callback()
        
  
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        #Creates a send message button.
        save_button = tk.Button(master=self, text="Send Message", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        #Creates an add user button.
        add_user = tk.Button(master=self, text="Add User.", width=7)
        add_user.configure(command=self.new_user)
        add_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=2)
  
        #Creates refresh  button.
        add_user = tk.Button(master=self, text="Refresh.", width=7)
        add_user.configure(command=self.refresh_msg)
        add_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=2)
      

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the Profile class
"""

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        self._draw() #Begins drawing all widgets.


    def send_message(self):
        """Sends a message to a recipient."""
        message = ds.DirectMessenger("168.235.86.101", 'test', 'test')
        message.send(self.body.get_text_entry(), self.body.recipient)
        self.body.set_text_entry(self.body.get_text_entry(), 'send') #Displays message on message viewer.
        #self.body.new_message()


    def add_user(self):
        """Creates a pop-up prompting the user to input a recipient name."""
        user = simpledialog.askstring(title="ADD USER", prompt="Enter Username:")
        if user == None:
            pass
        else:
            self.body.users.append(user) #Appends recipient name into list to keep track of who the user if currently messaging.
            self.body.insert_user(user) #Inserts recipient name onto treeview.
            #self.body.new_message()


    def refresh(self):
      """Refreshes messages if a node is selected on the treeview."""
      if self.body.recipient == None:
          pass
      else: self.body.new_message()


    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        #Adds a callback for sending messages and adding users.
        self.footer = Footer(self.root, save_callback=self.send_message, user_callback=self.add_user, refresh_callback=self.refresh)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)



if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    main.title("Messenger")
    main.geometry("500x400")
    main.option_add('*tearOff', False)

    MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
