import socket

def run_udp_client():
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    try:
        while True:
            message = input("Enter message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            # Send to server
            client_socket.sendto(message.encode(), server_address)
            
            # Wait for response (with timeout)
            client_socket.settimeout(2.0)  # Wait max 2 seconds
            try:
                response, _ = client_socket.recvfrom(1024)
                print(f"Server replied: {response.decode()}")
            except socket.timeout:
                print("Error: Server response timed out.")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_udp_client()