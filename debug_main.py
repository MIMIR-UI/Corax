import threading
from datetime import datetime

from config import NODE_ID, SERIAL_PORT, BAUD_RATE, ACK_TIMEOUT, MAX_RETRIES
from message import create_message, create_ack, encode_message, decode_message
import radio


SESSION_ID = ""
pending_acks = {}
seen_messages = set()
ack_lock = threading.Lock()
inbox = []
inbox_lock = threading.Lock()


# Converts packet time into local display time
def format_time(timestamp):
    time = datetime.fromisoformat(timestamp)
    local_time = time.astimezone()

    return local_time.strftime("%I:%M:%S %p")


# Displays the main Corax menu
def display_menu():
    with inbox_lock:
        inbox_count = len(inbox)

    print()
    print("================================")
    print(f"  CORAX // {SESSION_ID}")
    print("================================")
    print("[1] Send Message")
    print(f"[2] Inbox ({inbox_count})")
    print("[3] Settings")
    print("[4] Node Info")
    print("[Q] Quit")
    print("================================")


# Displays one inbox message
def display_message(message):
    print()
    print("--------------------------------")
    print("MESSAGE")
    print("--------------------------------")
    print(f"FROM: {message['sender']}")
    print(f"TIME: {format_time(message['timestamp'])}")
    print()
    print(message["text"])
    print("--------------------------------")

# Stores a received message in the inbox
def add_to_inbox(message):
    with inbox_lock:
        inbox.append(message)

    print()
    print(f"[NEW MESSAGE] From {message['sender']}")

# Displays the Corax inbox
def inbox_menu():
    while True:
        with inbox_lock:
            messages = list(inbox)

        print()
        print("================================")
        print("INBOX")
        print("================================")

        if not messages:
            print("Inbox empty.")
            print("================================")
            input("Press Enter to return...")
            return

        for index, message in enumerate(messages, start=1):
            print(
                f"[{index}] "
                f"{message['sender']} "
                f"- {format_time(message['timestamp'])}"
            )

        print("[B] Back")
        print("================================")

        choice = input("> ").strip().upper()

        if choice == "B":
            return

        try:
            message_number = int(choice)
        except ValueError:
            print("Invalid selection.")
            continue

        if message_number < 1 or message_number > len(messages):
            print("Invalid selection.")
            continue

        selected_message = messages[message_number - 1]

        display_message(selected_message)

        input("Press Enter to return to inbox...")


# Displays Corax settings
def settings_menu():
    print()
    print("================================")
    print("SETTINGS")
    print("================================")
    print(f"Session ID:   {SESSION_ID}")
    print(f"Serial Port:  {SERIAL_PORT}")
    print(f"UART Rate:    {BAUD_RATE}")
    print(f"ACK Timeout:  {ACK_TIMEOUT} seconds")
    print(f"Max Retries:  {MAX_RETRIES}")
    print("Frequency:    Not queried")
    print("TX Power:     Not queried")
    print("================================")
    input("Press Enter to return...")


# Displays physical node information
def node_info():
    print()
    print("================================")
    print("NODE INFORMATION")
    print("================================")
    print(f"Node ID:      {NODE_ID}")
    print(f"Session ID:   {SESSION_ID}")
    print("Radio:        ONLINE")
    print("================================")
    input("Press Enter to return...")


# Sends an acknowledgement for a received message
def send_ack(message):
    ack = create_ack(
        SESSION_ID,
        message["sender"],
        message["id"]
    )

    radio.send(encode_message(ack))


# Handles received Corax packets
def handle_packet(packet):
    packet_type = packet.get("type")

    if packet_type == "message":
        if packet["recipient"] not in (SESSION_ID, "ALL"):
            return

        message_id = packet["id"]

        if packet["recipient"] != "ALL":
            send_ack(packet)

        if message_id in seen_messages:
            return

        seen_messages.add(message_id)
        add_to_inbox(packet)

    elif packet_type == "ack":
        if packet["recipient"] != SESSION_ID:
            return

        message_id = packet["message_id"]

        with ack_lock:
            ack_event = pending_acks.get(message_id)

        if ack_event:
            ack_event.set()


# Listens continuously for incoming packets
def listen():
    while True:
        data = radio.receive()

        if not data:
            continue

        try:
            packet = decode_message(data)
            handle_packet(packet)

        except (UnicodeDecodeError, ValueError, KeyError):
            continue


# Sends a Corax message with delivery retries
def send_message():
    print()
    print("--------------------------------")
    print("SEND MESSAGE")
    print("--------------------------------")

    recipient = input("Recipient: ").strip().upper()

    if not recipient:
        print("Recipient cannot be empty.")
        return

    text = input("Message: ").strip()

    if not text:
        print("Message cannot be empty.")
        return

    message = create_message(
        SESSION_ID,
        recipient,
        text
    )

    message_id = message["id"]
    ack_event = threading.Event()

    with ack_lock:
        pending_acks[message_id] = ack_event

    total_attempts = MAX_RETRIES + 1

    for attempt in range(1, total_attempts + 1):
        radio.send(encode_message(message))

        print()
        print(f"Sent: {message_id}")

        if attempt > 1:
            print(f"Attempt: {attempt}/{total_attempts}")

        if ack_event.wait(ACK_TIMEOUT):
            print("Delivered.")
            break

        if attempt < total_attempts:
            print("No ACK received. Retrying...")

        else:
            print("Delivery failed.")

    with ack_lock:
        pending_acks.pop(message_id, None)


# Runs the Corax terminal interface
def main():
    global SESSION_ID

    print()
    print("================================")
    print("             CORAX")
    print("================================")

    while not SESSION_ID:
        SESSION_ID = input("Session ID: ").strip().upper()

    print()
    print(f"Session started as {SESSION_ID}")

    listener = threading.Thread(target=listen, daemon=True)
    listener.start()

    while True:
        display_menu()

        choice = input("> ").strip().upper()

        if choice == "1":
            send_message()

        elif choice == "2":
            inbox_menu()

        elif choice == "3":
            settings_menu()

        elif choice == "4":
            node_info()

        elif choice == "Q":
            break

        else:
            print("Invalid selection.")

    radio.close()


if __name__ == "__main__":
    main()
