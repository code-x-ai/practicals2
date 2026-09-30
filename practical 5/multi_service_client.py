import socket

HOST = "127.0.0.1"
PORT = 5004

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

print("=" * 55)
print("MULTI-CLIENT PROCESSING CLIENT")
print("=" * 55)

print("1. Calculate Factorial")
print("2. Generate Fibonacci Series")
print("3. Reverse Text")
print("4. Count Words")

print()
print("Type 'exit' to disconnect.")
print("=" * 55)

while True:
    operation = input("\nSelect operation: ").strip()

    # Exit from application
    if operation.lower() == "exit":
        client_socket.send("exit".encode())
        break

    # Factorial
    if operation == "1":
        value = input("Enter a number: ")

    # Fibonacci Series
    elif operation == "2":
        value = input("Enter number of terms: ")

    # Reverse Text
    elif operation == "3":
        value = input("Enter text: ")

    # Count Words
    elif operation == "4":
        value = input("Enter text: ")

    else:
        print("Invalid operation.")
        continue

    # Create request
    request = operation + "|" + value

    # Send request to server
    client_socket.send(request.encode())

    # Receive server response
    response = client_socket.recv(1024).decode()

    print()
    print("Server Response:", response)
    print("-" * 55)

# Close connection
client_socket.close()
print("Connection closed.")