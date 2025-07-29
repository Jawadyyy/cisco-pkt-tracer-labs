import socket

def send_video(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # ← FIXED (replace if needed)

    try:
        with open(file_path, "rb") as file:
            video_data = file.read()

        video_size = len(video_data)
        client_socket.sendall(video_size.to_bytes(8, byteorder='big'))

        chunk_size = 4096
        for i in range(0, len(video_data), chunk_size):
            chunk = video_data[i:i + chunk_size]
            client_socket.sendall(chunk)
        print(f"Sent {video_size} bytes")

        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    send_video("test_video.mp4")  # Replace with your video file