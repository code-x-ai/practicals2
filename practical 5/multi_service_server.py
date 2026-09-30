import socket
import threading

HOST = "127.0.0.1"
PORT = 5004   # Using 5004 to avoid clash with Practical 2 (5003)


def process_request(request):
    """Process the client request and return a response string."""
    try:
        operation, value = request.split("|", 1)

        # Operation 1: Factorial
        if operation == "1":
            number = int(value)
            if number < 0:
                return "Factorial is not defined for negative numbers."
            result = 1
            for i in range(1, number + 1):
                result *= i
            return f"Factorial of {number} is {result}"

        # Operation 2: Fibonacci Series
        elif operation == "2":
            number = int(value)
            if number <= 0:
                return "Please enter a positive number of terms."
            fibonacci = []
            a, b = 0, 1
            for _ in range(number):
                fibonacci.append(a)
                a, b = b, a + b
            return "Fibonacci Series: " + str(fibonacci)

        # Operation 3: Reverse Text
        elif operation == "3":
            reversed_text = value[::-1]
            return "Reversed Text: " + reversed_text

        # Operation 4: Count Words
        elif operation == "4":
            word_count = len(value.split())
            return f"Number of words: {word_count}"

        else:
            return "Invalid operation."

    except Exception as error:
        return "Error: " + str(error)


def handle_client(client_socket, client_address):
    """Handle a single client connection in a separate thread."""
    print(f"Client connected: {client_address}")

    while True:
        try:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            if data.lower() == "exit":
                break

            print(f"Request from {client_address}: {data}")

            result = process_request(data)
            client_socket.send(result.encode())

        except Exception:
            break

    client_socket.close()
    print(f"Client disconnected: {client_address}")


# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow immediate reuse of the port after restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind IP address and port
server_socket.bind((HOST, PORT))

# Start listening for clients
server_socket.listen()

print("=" * 55)
print("MULTI-CLIENT PROCESSING SERVER")
print("=" * 55)
print(f"Server running on {HOST}:{PORT}")
print("Waiting for clients...")
print("=" * 55)

# Accept multiple clients
while True:
    client_socket, client_address = server_socket.accept()

    # Create a separate thread for each client
    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    client_thread.start()