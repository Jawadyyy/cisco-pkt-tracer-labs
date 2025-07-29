import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    try:
        while True:
            message = input("Enter message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server replied: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()