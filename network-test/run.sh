#!/usr/bin/with-contenv bashio
# Copyright (C) 2026 Felix Gohringer (gpl-3.0-or-later)
set -euo pipefail

device=$(bashio::config 'device')
duration=$(bashio::config 'duration_minutes')
meter_id=$(bashio::config 'meter_id')
meter_arguments=()
if [[ -n "${meter_id}" ]]; then
    if [[ ! "${meter_id}" =~ ^[0-9]{8}$ ]]; then
        bashio::log.fatal "The unencrypted meter ID must contain exactly eight digits."
        exit 1
    fi
    meter_arguments=(WaterMeter auto "${meter_id}" NOKEY)
fi
case "${device}" in
    tcp://*|rfc2217://*) ;;
    *) bashio::log.fatal "Configure a tcp:// or rfc2217:// receiver address first."; exit 1 ;;
esac

bashio::log.info "Testing ${device} for ${duration} minutes."
/usr/bin/wmbusmeters --version
log_directory=/share/wmbusmeters-network-test
mkdir -p "${log_directory}"
log_file="${log_directory}/receiver-$(date -u +%Y%m%dT%H%M%SZ).log"
bashio::log.info "Persistent reception log: ${log_file}"
exec python3 /log_receiver.py "${log_file}" \
    /usr/bin/wmbusmeters --debug --logtelegrams --format=json \
    "--exitafter=${duration}m" "${device}" "${meter_arguments[@]}"
