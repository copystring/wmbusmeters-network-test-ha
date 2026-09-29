# Wmbusmeters network transport test for Home Assistant

Temporary diagnostic add-on for [wmbusmeters PR #2115](https://github.com/wmbusmeters/wmbusmeters/pull/2115).
It builds the exact tested network-serial revision and runs directly in Home Assistant.

Add this repository to the Home Assistant app store and install **[Test] Wmbusmeters RFC2217**.
Home Assistant builds the image locally. Configure `device`, for example
`rfc2217://bridge.local:20109:cul:t1`, then start the app and inspect its logs.
The test stops after 15 minutes by default; `duration_minutes` can be set up to 1440
for a 24-hour capture. It does not start automatically at boot.

The add-on tests receiver initialization and telegram reception without requiring a meter AES key.
It does not configure MQTT or create meter entities. It has no USB access and does not mount
Home Assistant configuration. Only one application may control the receiver.

Each run saves timestamped receiver output and raw telegrams to a new file under
`/share/wmbusmeters-network-test/`, while also showing the output in the app's log tab.
Files survive app restarts and updates. They are plain UTF-8 text and can be retrieved
through the Terminal & SSH app or an existing share browser. The timestamps use UTC.
Meter identifiers can be received without an AES key; encrypted measurements still
require the meter's key. No keys are stored by this diagnostic add-on.

To decode an unencrypted meter, set `meter_id` to its eight-digit ID. The add-on
uses automatic driver detection with `NOKEY` and logs the decoded JSON readings.
Water readings also receive a plain German summary with the total in cubic metres
and litres, and status messages. Leave `meter_id` empty for reception discovery.
Missing measurements are omitted from the summary; only fields broadcast by the
meter can be shown. Encrypted meter decoding is not configured by this option.

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
connection and were recognized. The owner confirmed that the received meter is
their unencrypted spare water meter. MQTT meter entities have not been configured
or validated.
