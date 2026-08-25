## Current End-Goal for v1.0

The current end goal for this project is to develop Corax into a reliable, portable, low-power text communication system capable of operating 
independently of existing network infrastructure.

Version 1.0 should provide multiple Corax nodes with the ability to send and receive addressed text messages over LoRa, identify users through 
temporary Session IDs, confirm successful message delivery, and maintain reliable communications in realistic field environments.

The system should be simple enough for a user to power on, select an identity, and begin communicating without requiring access to the 
Raspberry Pi terminal or development tools. The final v1.0 system should use a dedicated physical interface and enclosure suitable for portable field use.

Longer-term networking features should allow Corax nodes to relay traffic between one another, extending communication beyond the direct range of 
any individual node.

This end goal will change, expand, and develop over time.

## Development Goals for v0.2

Version 0.2 will focus on improving the current working point-to-point communication system and developing tools needed for continued testing.

* Improve message reliability and error handling.
* Maintain automatic acknowledgements, timeout detection, and message retransmission.
* Continue duplicate-message suppression to prevent retransmitted packets from appearing as new messages.
* Add a dedicated automated link-test function for range testing.
* Record packet delivery rate, failed packets, retry count, and round-trip time during link tests.
* Add basic message and system logging for later review during testing.
* Improve packet validation and begin formalizing the Corax message protocol.
* Add a protocol version field to transmitted packets.
* Improve management of stored message IDs and other temporary runtime data.
* Continue development of the debug interface for testing radio, messaging, and node functions.
* Investigate reading radio configuration information such as operating frequency and transmit-power setting.
* Begin designing packet fields and software architecture needed for future multi-node relay and mesh functionality.
* Conduct additional range and obstruction testing using the existing two-node system.


