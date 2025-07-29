import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Client")
        
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)
        
        tk.Label(connection_frame, text="Server IP:").grid(row=0, column=0, padx=5)
        self.server_ip_entry = tk.Entry(connection_frame, width=15)
        self.server_ip_entry.grid(row=0, column=1, padx=5)
        self.server_ip_entry.insert(0, "localhost")
        
        tk.Label(connection_frame, text="Port:").grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(connection_frame, width=5)
        self.port_entry.grid(row=0, column=3, padx=5)
        self.port_entry.insert(0, "5555")
        
        tk.Label(connection_frame, text="Your Name:").grid(row=0, column=4, padx=5)
        self.name_entry = tk.Entry(connection_frame, width=15)
        self.name_entry.grid(row=0, column=5, padx=5)
        self.name_entry.insert(0, "User")
        
        self.connect_button = tk.Button(connection_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=6, padx=5)
        
        self.disconnect_button = tk.Button(connection_frame, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=7, padx=5)
        
        self.chat_area = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled')
        self.chat_area.pack(padx=10, pady=10)
        
        message_frame = tk.Frame(self.root)
        message_frame.pack(pady=10)
        
        self.message_entry = tk.Entry(message_frame, width=50)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        
        self.send_button = tk.Button(message_frame, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def log_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
        
    def connect_to_server(self):
        try:
            server_ip = self.server_ip_entry.get()
            port = int(self.port_entry.get())
            self.client_socket.connect((server_ip, port))
            
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.log_message(f"Connected to {server_ip}:{port}")
            
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            # Send the client's name to the server
            name = self.name_entry.get()
            self.client_socket.send(f"{name} joined the chat".encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            
    def disconnect(self):
        try:
            name = self.name_entry.get()
            self.client_socket.send(f"{name} left the chat".encode('utf-8'))
            self.client_socket.close()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            self.send_button.config(state=tk.DISABLED)
            self.log_message("Disconnected from server")
        except:
            pass
            
    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                name = self.name_entry.get()
                full_message = f"{name}: {message}"
                self.client_socket.send(full_message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except:
                self.log_message("Failed to send message")
                self.disconnect()
                
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.log_message(message)
            except:
                self.log_message("Connection lost")
                self.disconnect()
                break
                
    def on_closing(self):
        self.disconnect()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()