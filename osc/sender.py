from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 9000)  # IP and port of the receiver
value = 0

while True:
    client.send_message("/number", value)  # Send the current value to the receiver
    print(f"Sent value: {value}")  # Print the sent value and its type
    value += 1  # Increment the value for the next message
    time.sleep(1)  # Wait for 1 second before sending the next message