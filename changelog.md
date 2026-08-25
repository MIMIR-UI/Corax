# Changelog

All notable changes to Project Corax will be documented here.

## [Unreleased]

### Added
- Automated link-test mode planned for range testing.
- Protocol version field planned for transmitted packets.
- Message logging and test-result logging planned.

### Changed
- Continued cleanup of project structure and documentation.

---

## [v0.2.0] - In Development

### Added
- Session IDs for temporary user addressing.
- Message acknowledgements (ACKs).
- Automatic ACK timeout and retransmission.
- Duplicate-message suppression.
- Inbox for received messages.
- Broadcast addressing using `ALL`.
- Human-readable local timestamps.
- Basic settings and node-information menus.
- Debug terminal interface for sending, receiving, and reviewing messages.
- Message delivery status reporting.

### Changed
- Corax messages now use structured JSON packets.
- Message IDs increased to 12 hexadecimal characters.
- Sender identity separated from permanent physical node identity.
- Radio communication moved into a dedicated `radio.py` module.
- Radio and UART settings moved into `config.py`.

### Verified
- Bidirectional point-to-point LoRa messaging between two Corax nodes.
- Repeated message transmission and reception.
- ACK and retry functionality.
- UART communication between Raspberry Pi and E22/SX1262 LoRa HAT.

---

## [v0.1.0]

### Added
- Initial Corax Python project structure.
- Basic Raspberry Pi node configuration.
- Unique message IDs.
- UTC timestamps.
- JSON message encoding and decoding.
- UART communication over `/dev/serial0`.
- Basic LoRa transmit and receive functionality.
- Direct text messaging between two Corax nodes.
