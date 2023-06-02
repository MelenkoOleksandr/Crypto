import ssl
import socket

def handle_client(client_socket):
    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='certificate.crt', keyfile='private.key')

    # Wrap the client socket with the SSL context
    ssl_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)

    # Perform SSL handshake
    ssl_client_socket.do_handshake()

    # Send and receive encrypted data
    encrypted_data = ssl_client_socket.recv(1024)
    decrypted_data = encrypted_data.decode()
    print("Received from client:", decrypted_data)

    message = "Hello, client!"
    ssl_client_socket.send(message.encode())

    # Close the SSL connection
    ssl_client_socket.close()

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind(('localhost', 1234))

# Listen for incoming connections
server_socket.listen(1)
print("Server listening on port 1234...")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    # Handle the client connection in a separate function
    handle_client(client_socket)
