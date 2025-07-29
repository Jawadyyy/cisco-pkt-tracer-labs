import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatServer:
    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Server")
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_button = tk.Button(control_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(control_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.log_area = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled')
        self.log_area.pack(padx=10, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)
        
    def start_server(self):
        try:
            self.server_socket.bind(('0.0.0.0', 5555))
            self.server_socket.listen(5)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_message("Server started on port 5555")
            
            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()
        except Exception as e:
            self.log_message(f"Error starting server: {e}")
            
    def stop_server(self):
        for client in self.clients:
            client[0].close()
        self.clients = []
        self.server_socket.close()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("Server stopped")
        
    def accept_connections(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                self.clients.append((client_socket, addr))
                self.log_message(f"New connection from {addr}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()
            except:
                break
                
    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                self.log_message(f"Message from {addr}: {message}")
                self.broadcast(message, addr)
            except:
                break
                
        client_socket.close()
        self.clients.remove((client_socket, addr))
        self.log_message(f"Client {addr} disconnected")
        
    def broadcast(self, message, sender_addr):
        for client in self.clients:
            if client[1] != sender_addr: 
                try:
                    client[0].send(message.encode('utf-8'))
                except:
                    client[0].close()
                    self.clients.remove(client)
                    
    def on_closing(self):
        self.stop_server()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    server = ChatServer()
    server.run()