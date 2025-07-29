import socket
import threading

def handle_client(connection, client_address):
    try:
        print(f"\nConnection from {client_address}")
        
        # 1. Receive image size first (as a 4-byte integer)
        image_size_bytes = connection.recv(4)
        image_size = int.from_bytes(image_size_bytes, byteorder='big')
        print(f"Receiving {image_size} bytes from {client_address}")

        # 2. Receive image data in chunks
        received_data = b''
        while len(received_data) < image_size:
            chunk = connection.recv(1024)
            if not chunk:
                break
            received_data += chunk

        # 3. Save the image
        with open(f"received_image_{client_address[1]}.jpg", "wb") as file:
            file.write(received_data)
        print(f"Image saved from {client_address}")

        # 4. Send acknowledgment
        connection.sendall(b"Image received successfully!")

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        connection.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started. Waiting for clients...")

    try:
        while True:
            connection, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(connection, client_address),
                daemon=True
            )
            thread.start()
            print(f"Active threads: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()