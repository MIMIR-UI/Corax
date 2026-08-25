# Project Corax
# Named because, yknow, raven. Duh. EW. Moving on.

Corax is a Raspberry Pi–based low-power text communications project using SX1262/E22-series LoRa radio hardware. The current goal is simple, reliable point-to-point messaging between portable nodes, with the architecture designed so additional capabilities can be added later.

## Current Hardware
- Raspberry Pi 3 Model A+
- E22/SX1262 LoRa HAT
- 915 MHz radio hardware
- microSD-based Raspberry Pi OS
- Headless operation over SSH during development

## Current Software Capabilities
- Bidirectional text messaging between two Corax nodes
- Session IDs/callsigns for addressing users during a session
- Unique message IDs
- UTC timestamps with human-readable local display time
- Message acknowledgements (ACKs)
- Automatic ACK timeout and retransmission
- Duplicate-message suppression
- Basic inbox for received messages
- Broadcast addressing using `ALL`
- Temporary/debug terminal interface
- Separate configuration, messaging, and radio modules

## Current Architecture
- `main.py` — debug interface and application flow
- `message.py` — message creation, encoding, decoding, and ACK packets
- `radio.py` — UART communication with the LoRa radio
- `config.py` — node and communication settings

Corax currently communicates with the radio over UART at 9600 baud. Messages are serialized as JSON, converted to bytes, transmitted over LoRa, reconstructed by the receiving node, and acknowledged back to the sender.

## Development Status
The basic point-to-point communications layer is functional and stable under repeated messaging. Current development is focused on improving testing tools, message handling, protocol structure, and reliability before expanding toward additional networking capabilities.

