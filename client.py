from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
# import tkinter

client_socket = None
top = None
def receive():
    global top, client_socket
    BUFSIZ = 1024

    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            
            top.displayTextBox.configure(state="normal")
            top.displayTextBox.insert(tk.END, msg)
            top.displayTextBox.configure(state="disabled")
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break


def send():  # event is passed by binders.
    global top, client_socket
    '''
    """Handles sending of messages."""
    # msg = my_msg.get()
    name = input("name: ")
    client_socket.send(bytes(name, "utf8"))
    connection = True
    while connection:
    '''
    msg = top.msgTextBox.get("1.0", tk.END)
    client_socket.send(bytes(msg, "utf8"))
    top.msgTextBox.delete("1.0", tk.END)  # Clears input field.
    if msg == "q":
        client_socket.close()
        top.quit()


def sendThreadFunc():    
    send_thread = Thread(target = send)
    send_thread.start()
def enterPressed(keypressed):    
    send_thread = Thread(target = send)
    send_thread.start()
'''
GUI
'''
def createChatClient(HOST,PORT):
    global client_socket, top
    top = tk.Tk()
    color = '#d9d9d9'  # X11 color: 'gray85'
    _fgcolor = '#000000'  # X11 color: 'black'
    _compcolor = '#d9d9d9' # X11 color: 'gray85'
    _ana1color = '#d9d9d9' # X11 color: 'gray85' 
    _ana2color = '#ececec' # Closest X11 color: 'gray92' 

    top.geometry("388x433+461+125")
    top.title("Chat")
    top.configure(background="#d9d9d9")
    top.chatFrame = tk.Frame(top)
    top.chatFrame.place(relx=0.0, rely=0.0, relheight=0.982, relwidth=0.992)

    top.chatFrame.configure(relief='groove')
    top.chatFrame.configure(borderwidth="2")
    top.chatFrame.configure(relief='groove')
    top.chatFrame.configure(background="#d9d9d9")
    top.chatFrame.configure(width=385)



    top.msgTextBox = tk.Text(top.chatFrame)
    top.msgTextBox.place(relx=0.026, rely=0.8, relheight=0.193, relwidth=0.774)
    top.msgTextBox.configure(background="white")
    top.msgTextBox.configure(font="TkTextFont")
    top.msgTextBox.configure(foreground="black")
    top.msgTextBox.configure(highlightbackground="#d9d9d9")
    top.msgTextBox.configure(highlightcolor="black")
    top.msgTextBox.configure(insertbackground="black")
    top.msgTextBox.configure(selectbackground="#c4c4c4")
    top.msgTextBox.configure(selectforeground="black")
    top.msgTextBox.configure(width=298)
    top.msgTextBox.configure(wrap='word')
    top.msgTextBox.bind("<Return>", enterPressed)


    top.sendButton = tk.Button(top.chatFrame)
    top.sendButton.place(relx=0.805, rely=0.871, height=22, width=71)
    top.sendButton.configure(activebackground="#ececec")
    top.sendButton.configure(activeforeground="#000000")
    top.sendButton.configure(background="#d9d9d9")

    top.sendButton.configure(foreground="#000000")
    top.sendButton.configure(highlightbackground="#d9d9d9")
    top.sendButton.configure(highlightcolor="black")
    top.sendButton.configure(text='''Send''')
    top.sendButton.configure(width=71)


    top.displayTextBox = tk.Text(top.chatFrame)
    top.displayTextBox.place(relx=0.0, rely=0.024, relheight=0.758, relwidth=0.982)
    top.displayTextBox.configure(background="#000000")
    top.displayTextBox.configure(font="TkTextFont")
    top.displayTextBox.configure(foreground="#ffffff")
    top.displayTextBox.configure(highlightbackground="#d9d9d9")
    top.displayTextBox.configure(highlightcolor="black")
    top.displayTextBox.configure(insertbackground="black")
    top.displayTextBox.configure(selectbackground="#c4c4c4")
    top.displayTextBox.configure(selectforeground="black")
    top.displayTextBox.configure(state='disabled')
    top.displayTextBox.configure(width=378)
    top.displayTextBox.configure(wrap='word')

    top.sendButton.configure(command=sendThreadFunc)

    #----Now comes the sockets part----

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    top.mainloop()  # Starts GUI execution.
