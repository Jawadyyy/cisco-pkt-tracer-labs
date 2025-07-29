import socket

def start_udp_server():
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    print("UDP Server started. Waiting for messages...")

    try:
        while True:
            # Receive data (max 1024 bytes) and client address
            data, client_address = server_socket.recvfrom(1024)
            data = data.decode()
            print(f"Received from {client_address}: {data}")

            # Process data (e.g., uppercase)
            response = data.upper().encode()
            server_socket.sendto(response, client_address)
            print(f"Sent back to {client_address}: {response.decode()}")
    
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_udp_server()