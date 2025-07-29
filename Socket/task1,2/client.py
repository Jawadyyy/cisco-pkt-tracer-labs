import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
print(f"Connecting to {server_address[0]}:{server_address[1]}...")
client_socket.connect(server_address)

try:
    # Send lowercase message
    message = input("Enter a lowercase message: ")
    client_socket.sendall(message.encode())
    print(f"Sent: {message}")
    
    # Receive the server's response
    response = client_socket.recv(1024).decode()
    print(f"Server replied: {response}")

finally:
    # Close the connection
    client_socket.close()