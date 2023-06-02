import ssl
import socket

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_client_socket = ssl_context.wrap_socket(socket.socket(
    socket.AF_INET, socket.SOCK_STREAM), server_hostname='localhost')

# Perform SSL handshake
ssl_client_socket.connect(('localhost', 1234))

# Send encrypted data
message = "Hello, server!"
ssl_client_socket.send(message.encode())

# Receive encrypted data
encrypted_response = ssl_client_socket.recv(1024)
decrypted_response = encrypted_response.decode()
print("Received from server:", decrypted_response)

# Close the SSL connection
ssl_client_socket.close()
