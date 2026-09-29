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

## Validation on 2026-09-29

Version 0.1.1 was built and started in an amd64 Home Assistant installation.
The build passed the C++ internal tests and all seven network integration tests,
including real ser2net in raw TCP and RFC2217 modes. A physical nanoCUL868 running
firmware 1.67 (`nanoCUL868_r571`) accepted RFC2217 configuration and confirmed
both `TMODE` and `CMODE` when initialized by the add-on. In C1 mode, real
Kamstrup cold-water meter telegrams reached wmbusmeters through the RFC2217
connection and were recognized. Ownership of the received meter has not been
confirmed. MQTT meter entities have not been configured or validated.
