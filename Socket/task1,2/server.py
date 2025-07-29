import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
print(f"Starting server on {server_address[0]}:{server_address[1]}")
server_socket.bind(server_address)

# Listen for incoming connections (max 1 connection in queue)
server_socket.listen(1)

while True:
    print("\nWaiting for a client connection...")
    connection, client_address = server_socket.accept()
    
    try:
        print(f"Connection established with {client_address}")
        
        # Receive data (max 1024 bytes)
        data = connection.recv(1024).decode()
        if data:
            print(f"Received: {data}")
            
            # Convert to uppercase and send back
            response = data.upper()
            connection.sendall(response.encode())
            print(f"Sent back: {response}")
        else:
            print("No data received. Closing connection.")
    
    finally:
        # Clean up the connection
        connection.close()