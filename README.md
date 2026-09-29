# Wmbusmeters network transport test for Home Assistant

Temporary diagnostic add-on for [wmbusmeters PR #2115](https://github.com/wmbusmeters/wmbusmeters/pull/2115).
It builds the exact tested network-serial revision and runs directly in Home Assistant.

Add this repository to the Home Assistant app store and install **[Test] Wmbusmeters RFC2217**.
Home Assistant builds the image locally. Configure `device`, for example
`rfc2217://bridge.local:20109:cul:t1`, then start the app and inspect its logs.
The test stops after 15 minutes by default. It does not start automatically at boot.

The add-on tests receiver initialization and telegram reception without requiring a meter AES key.
It does not configure MQTT or create meter entities. It has no USB access and does not mount
Home Assistant configuration or shared volumes. Only one application may control the receiver.

During the local image build, Home Assistant runs protocol tests and both transports against real ser2net,
and verifies the runtime binary. The transport itself is GPL-3.0-or-later; its source is pinned in the Dockerfile.

Co-authored with an AI agent (OpenAI Codex).
