import socket
import threading

def handle_client(connection, client_address):
    try:
        print(f"\nNew connection from {client_address}")
        
        while True:
            data = connection.recv(1024).decode()
            if not data:  # Client disconnected
                break
            
            print(f"Received from {client_address}: {data}")
            
            # Process data (e.g., convert to uppercase)
            response = data.upper()
            connection.sendall(response.encode())
            print(f"Sent back to {client_address}: {response}")
    
    except ConnectionResetError:
        print(f"Client {client_address} disconnected abruptly.")
    finally:
        connection.close()
        print(f"Connection with {client_address} closed.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)  # Allow up to 5 pending connections
    print("Server started. Waiting for clients...")

    try:
        while True:
            connection, client_address = server_socket.accept()
            # Start a new thread for each client
            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, client_address),
                daemon=True
            )
            client_thread.start()
            print(f"Active threads: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()