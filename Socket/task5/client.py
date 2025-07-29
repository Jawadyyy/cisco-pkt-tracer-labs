import socket

def send_image(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    try:
        # 1. Read image in binary mode
        with open(file_path, "rb") as file:
            image_data = file.read()

        # 2. Send image size first (4-byte big-endian integer)
        image_size = len(image_data)
        client_socket.sendall(image_size.to_bytes(4, byteorder='big'))

        # 3. Send image data in chunks
        client_socket.sendall(image_data)
        print(f"Sent {image_size} bytes")

        # 4. Wait for acknowledgment
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    send_image("test_image.jpg")  # Replace with your image path