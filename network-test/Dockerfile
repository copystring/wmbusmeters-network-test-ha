# Copyright (C) 2026 Felix Gohringer (gpl-3.0-or-later)
ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM ${BUILD_FROM} AS build

RUN apk add --no-cache build-base git pkgconf linux-headers \
    libxml2-dev libxslt-dev librtlsdr-dev libusb-dev bash jq python3 ser2net

# Build the exact revision that passed the upstream PR's Linux regression suite.
WORKDIR /src
RUN git init && \
    git remote add origin https://github.com/copystring/wmbusmeters.git && \
    git fetch --depth 1 origin 5648f50439218acb8bfc71340a06d41e4f16a7a1 && \
    git checkout --detach FETCH_HEAD
RUN ./configure && make -j2 TAG=3.0.0-network-test

ARG RUN_TESTS=true
RUN if [ "${RUN_TESTS}" = "true" ]; then \
    build/testinternals && python3 tests/test_network_serial.py build/wmbusmeters; \
    fi

FROM ${BUILD_FROM} AS runtime
RUN apk add --no-cache libstdc++ libxml2 libxslt librtlsdr libusb
COPY --from=build /src/build/wmbusmeters /usr/bin/wmbusmeters
COPY run.sh /run.sh
RUN chmod 755 /run.sh && /usr/bin/wmbusmeters --version
CMD ["/run.sh"]
