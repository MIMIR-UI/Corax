from datetime import datetime, timezone
import json
import uuid


# Creates a Corax text message
def create_message(sender, recipient, text):
    return {
        "type": "message",
        "id": uuid.uuid4().hex[:12],
        "sender": sender,
        "recipient": recipient,
        "text": text,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
    }


# Creates an acknowledgement for a received message
def create_ack(sender, recipient, message_id):
    return {
        "type": "ack",
        "id": uuid.uuid4().hex[:12],
        "sender": sender,
        "recipient": recipient,
        "message_id": message_id,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
    }


# Converts a Corax packet into bytes
def encode_message(message):
    return json.dumps(message).encode("utf-8")


# Converts received bytes into a Corax packet
def decode_message(data):
    return json.loads(data.decode("utf-8"))
