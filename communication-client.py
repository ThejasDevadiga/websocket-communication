import asyncio
import websockets
import tkinter as tk
from threading import Thread
import customtkinter as ctk
from tkinter import messagebox
import re

class WebSocketUI:
    def __init__(self, master,uri):
        self.master = master
        master.title("ALCUIN Client")
        self.master.geometry(f"{850}x{600}")
        self.master.resizable(0, 0)
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=3)
        self.master.columnconfigure(4,weight=3)
        self.master.configure(background="#070f24")
        self.uri =tk.StringVar()
        self.uri.set(uri)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.connect_status = tk.StringVar()
        self.connect_status.set("Not connected")
        self.conn = False
        self.message = tk.StringVar()
        self.sent_messages = []
        self.received_messages = []
        self.uri_label =  tk.Label(master, text="URI:",fg='white',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.uri_name =  tk.Label(master,  textvariable=self.uri,fg='green',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.uri_changer =  ctk.CTkButton(master, text="Change", fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"), command=self.change_uri)
        self.message_label =  tk.Label(master, text="Message:",fg='white',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.message_entry = ctk.CTkEntry(master, placeholder_text="Enter the data here")
        self.send_button = ctk.CTkButton(master, text="Send", fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"), command=self.send_message)
        self.sent_messages_label =  tk.Label(master, text="Sent Messages :",fg='white',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.sent_messages_text = tk.Text(master, height=10, width=50,bg="#adadad",fg="#041f66",borderwidth=2)
        self.received_messages_label = tk.Label(master, text="Recieved Message:",fg='white',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.received_messages_text = tk.Text(master, height=10, width=50,bg="#adadad",fg="#041f66",borderwidth=2)
        self.connect_label = ctk.CTkLabel(master, text="Connection Status :",font=ctk.CTkFont(size=15, weight="bold"))
        self.connect_status_label =  tk.Label(master,  textvariable=self.connect_status,fg='red',bg="#070f24", font=ctk.CTkFont(size=20, weight="bold"))
        self.exit_button = ctk.CTkButton(master, text="Exit",command=self.close, fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"))
        self.reconnect_button = ctk.CTkButton(master, text="Reconect",command=self.reconnect, fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"))
        self.sent_messages_text.configure(state="disabled")
        self.received_messages_text.configure(state="disabled")

        self.uri_label.grid(row=0,column=0,padx=(50,50),pady=(10,10))
        self.uri_name.grid(row=0,column=1)
        self.uri_changer.grid(row=0,column=4)

        self.message_label.grid(row=1, column=0 ,padx=(50,50), pady=(20,20))
        self.message_entry.grid(row=1, column=1,)
        self.send_button.grid(row=1, column=4 ,padx=20)

        self.sent_messages_label.grid(row=2, column=0)
        self.sent_messages_text.grid(row=2, column=1, columnspan=3,padx=(10,10), pady=(10,10))

        self.received_messages_label.grid(row=4, column=0,padx=20)
        self.received_messages_text.grid(row=4, column=1, columnspan=3,padx=(10,10), pady=(10,10))

        self.connect_label.grid(row=6, column=0)
        self.connect_status_label.grid(row=6, column=1)
        self.reconnect_button.grid(row=6,column=4)

        self.exit_button.grid(row=8, column=4,padx=20,pady=30)

        self.socket = None

    def change_uri(self):
        self.master.destroy()
        con = tk.Tk()
        AlcuinConnector(con)
        con.mainloop()
        
    def reconnect(self):
        if not self.conn:
            # self.master.destroy()
            # con = tk.Tk()
            # AlcuinConnector(con)
            # con.mainloop()
            self.start(self.uri)
            
    def hideReconn(self):
        self.reconnect_button.grid_forget()
    
    def showReconn(self):
        self.reconnect_button.grid(row=6,column=4)

    def show_alert(self,title,message):
        messagebox.showinfo(title, message)  

    async def connect_socket(self,uri):
        try:
            self.socket = await websockets.connect(uri)
            self.connect_status.set("Connected")
            self.conn = True
            self.connect_status_label.configure(fg='green')
            self.hideReconn()
            # asyncio.ensure_future(self.socket.send("Device : PC"))
            while True:
                message = await self.socket.recv()
                self.received_messages.append(message)
                self.received_messages_text.configure(state="normal")
                self.received_messages_text.insert(tk.END,"Recieved :"+ message + "\n")
                self.received_messages_text.configure(state="disabled")
        except Exception as e:
            print(e)
            self.connect_status_label.configure(fg='red')
            self.conn = False
            self.connect_status.set("Disconnected")
            self.showReconn()
            self.socket = None

    def send_message(self):
        message = self.message_entry.get()
        if not self.conn:
            self.show_alert("Alert","Please connect to the server")
            self.message_entry.delete(0, tk.END)
            return
        if message=="":
            self.show_alert("Alert","Please enter some data")
            return
        if self.socket:
            asyncio.run(self.socket.send(message))
            self.sent_messages.append(message)
            self.sent_messages_text.configure(state="normal")
            self.sent_messages_text.insert(tk.END,"Sent :"+message + "\n")
            # self.message_entry.delete(0, tk.END)
            self.sent_messages_text.configure(state="disabled")

    def start(self,uri):
        self.uri = uri
        self.connThread=Thread(target=self.run,args=(uri,), daemon=True)
        self.connThread.start()

    def run(self,uri):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_socket(uri))

    def close(self): 
        try:
            if self.socket:
                self.master.destroy()
                asyncio.run(self.socket.close())
        except ValueError :
                print("Closing.....")
class AlcuinConnector:
    def __init__(self, root):
        self.root = root
        self.root.title("ALCUIN BOT")
        self.root.geometry(f"{800}x{300}")
        root.configure(background="#070f24")
        root.resizable(0, 0)

      
        self.logo_label = ctk.CTkLabel(self.root, text=" ALCUIN CONNECTION ", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=3, padx=(250,50), pady=(50, 50))

        self.entry = ctk.CTkEntry(self.root, placeholder_text="Enter the data here")
        self.entry.grid(row=2, column=1, columnspan=3, padx=(50, 50), pady=(0,0), sticky="nsew")
        
        
        self.main_button_1 = ctk.CTkButton(master=self.root, fg_color="transparent",text="Connect",command=self.connect, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=2, column=4,padx=50 , sticky="nsew")
        self.exit_button = ctk.CTkButton(master=self.root, fg_color="transparent",text="Exit",command=exit, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.exit_button.grid(row=4, column=4,padx=50, pady=30 ,sticky="nsew")
    def show_alert(self,title,message):
        messagebox.showinfo(title, message)   
    def connect(self):
        regex = r"^wss?://[\w.-]+(:\d+)?(/[\w./]*)?$"
        val = self.entry.get()
        if val=="":
            self.show_alert("Alert","Please enter some data")
        elif re.match(regex, val) or True:
            val="ws://192.168.37.228:3000/"
            # val="ws://localhost:8765/"
            print(val)
            self.root.destroy()
            root = tk.Tk()
            ui = WebSocketUI(root,val)
            ui.start(val)
            root.mainloop()
        else:
            self.show_alert("Alert","Invalid URL")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    con = tk.Tk()
    AlcuinConnector(con)
    con.mainloop()

