# https://amzn.eu/d/6zTYaFN
# cust-tkinter.py
import tkinter
import tkinter.messagebox
import customtkinter
import asyncio
import websockets
import re

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Communication")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Tab 2"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(10, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

        

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")













import threading
import json

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# https://github.com/TomSchimansky/CustomTkinter
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
websocket = None



class Main(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #  Connection status
        self.connection = False
        self.connection_string = None
        # configure window
        self.title("ALCUIN BOT")
        self.geometry(f"{900}x{500}")

        # configure grid layout (4x4)
        
        self.grid_columnconfigure((2,2), weight=1)
        self.grid_rowconfigure((0, 1, 1), weight=1)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter the data here")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",text="Send",command=self.send_string, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=" SOCKET ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Connect", command=self.get_connection_string)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="disconnect",command=self.disconnect_server)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="status",command=self.get_connection_status)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

 
        self.sendBox = customtkinter.CTkTextbox(self, width=190, font=("Helvetica", 16))
        self.sendBox.grid(row=0, column=1, padx=(20,0), pady=(20, 20), sticky="nsew")
        self.sendBox.configure(state="disabled")
        
        self.chatBox = customtkinter.CTkTextbox(self, width=50, font=("Helvetica", 16))
        self.chatBox.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.chatBox.configure(state="disabled")

        self.recieveBox = customtkinter.CTkTextbox(self, width=190, font=("Helvetica", 16))
        self.recieveBox.grid(row=0, column=3, padx=(20,20), pady=(20, 20), sticky="nsew")
        self.recieveBox.configure(state="disabled")

    def disconnect_server(self):
        global websocket
        websocket = None
        self.connection_string =  None
        self.insert_to_chatBox("Server disconnected !!")
        self.connection = False

    def send_string(self):
        data = self.entry.get()
        if self.connection:
            if self.send_data_Server(data):
                self.insert_to_sendBox(data)
            else:
                self.insert_to_chatBox("Error while sending data !!")
        else:
            self.insert_to_chatBox("Not connected to server !!")
    
    def get_connection_status(self):
        
        if self.connection:
            data ="Connected to "+str(self.connection_string)
        else:
            data ="Disconnected "
        dialog = customtkinter.CTkInputDialog(text=data, title="Connection")

    def send_data_Server(self,data):
        if asyncio.get_event_loop().run_until_complete(send_data(data)):
            self.insert_to_recvBox(asyncio.get_event_loop().run_until_complete(recv_data()))
            return True
        return False
            
    def get_connection_string(self):
        dialog = customtkinter.CTkInputDialog(text="Enter connection ulr!  : ws://localhost:8765/ ", title="Connection")
        data = dialog.get_input()
        self.connection = True
        if data:
            print("Connection url is : ",data)
            self.insert_to_chatBox("Connecting...........\n")
            self.insert_to_chatBox( "host :"+data+'\n')
            if self.make_connection(data):
                self.insert_to_chatBox("Connection successful!\n")
            else:
                self.insert_to_chatBox("Connection failed!")
                self.connection = False
    
    def clear_text_box(self):
        print("clear text box")

    def insert_to_chatBox(self,data):
        data = str(data)
        self.chatBox.configure(state="normal")
        if self.connection:
            self.chatBox.insert('200.2000','\n'+data+'\n')
        else:
            self.chatBox.insert('200.2000',"\nPlease connect to the server !!!\n")
        self.chatBox.configure(state="disabled")
        return 
    
    def insert_to_sendBox(self,data):
        data = str(data)
        self.sendBox.configure(state="normal")
        if self.connection:
            self.sendBox.insert('200.2000','\n'+data+'\n')
        else:
            self.sendBox.insert('200.2000',"\nPlease connect to the server !!!\n")
        self.sendBox.configure(state="disabled")

    def insert_to_recvBox(self,data):
        data = str(data)
        self.recieveBox.configure(state="normal")
        if self.connection:
            self.recieveBox.insert('200.2000','\n'+data+'\n')
        else:
            self.recieveBox.insert('200.2000',"\nPlease connect to the server !!!\n")
        self.recieveBox.configure(state="disabled")
         
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def make_connection(self,url):
        regex = r"^wss?://[\w.-]+(:\d+)?(/[\w./]*)?$"
        if re.match(regex, url):
            data = asyncio.get_event_loop().run_until_complete(connect_to_websocket(url))
            
            if data=='True':
                self.connection_string = url
                return True
            self.insert_to_chatBox('\n'+data)
            return False
        self.insert_to_chatBox("Enter the valid url\n")
        return False

    def sidebar_button_event(self):

        print("sidebar_button click")


def connect_ws():
    global ws

    def on_open(ws):
        ji = {
            "isfirst": "true",
            "device": "pc"
        }
        ws.send(json.dumps(ji))
        
    def on_message(ws, message:str):
        global app
        global prv_position
        pat = r"\(\d+,\d+\)"
        if re.match(pat,message):
            msg = message.replace("(","").replace(")","").split(",") 
            pos = (int(msg[0]),int(msg[1]))
            if prv_position ==None:
                prv_position = pos
            app.bot_tracker(position=pos)
            # print("del lines : ",prv_position,pos)
            app.delete_line(prv_position,pos)
            app.delete_img(prv_position)
            prv_position = pos
       
        response = json.loads(message)
        conection = response["conection"]
        print("conection: ", conection)
        if conection == "true":
            print("Connection Established")
            devices = json.loads(response["devices"])
            print(f"Mobile: {devices['mobile']}\tPC: {devices['pc']}\tESP: {devices['ESP']}")

        elif conection == "newConnection" or conection == "lost":
            devices = json.loads(response["devices"])
            print(f"Mobile: {devices['mobile']}\tPC: {devices['pc']}\tESP: {devices['ESP']}")

        elif conection == "Sending":
            devices = json.loads(response["devices"])
            print(f"Mobile: {devices['mobile']}\tPC: {devices['pc']}\tESP: {devices['ESP']}")
            
        elif conection == "alreadyConected" or conection == "close":
            ws.close()
        
    def on_close(ws):
        print("Close connection")
        ws.close()  
    ws = websocket.WebSocketApp('ws://localhost:8765/', on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    ws_thread = threading.Thread(target=connect_ws) 
    ws_thread.start()
    app = Main()
    app.mainloop()
