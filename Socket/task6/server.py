import socket
import threading
import os

def handle_client(connection, client_address):
    try:
        print(f"\nConnection from {client_address}")
        
        # 1. Receive video file name and size (first 8 bytes for size)
        header = connection.recv(8)
        video_size = int.from_bytes(header, byteorder='big')
        print(f"Receiving {video_size} bytes from {client_address}")

        # 2. Receive video data in chunks
        received_data = b''
        while len(received_data) < video_size:
            chunk = connection.recv(4096)  # Larger chunk size for videos
            if not chunk:
                break
            received_data += chunk

        # 3. Save the video with a unique name
        video_name = f"received_video_{client_address[1]}.mp4"
        with open(video_name, "wb") as file:
            file.write(received_data)
        print(f"Video saved as {video_name}")

        # 4. Send acknowledgment
        connection.sendall(b"Video received successfully!")

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        connection.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Allow external connections
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