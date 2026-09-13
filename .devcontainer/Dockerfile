FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        ffmpeg \
        freerdp3-x11 \
        gh \
        pulseaudio \
        pulseaudio-utils \
        python3-pip \
        python3-venv \
        software-properties-common \
        tigervnc-standalone-server \
        tigervnc-tools \
        v4l2loopback-dkms \
        websockify \
        xfce4 \
        xfce4-goodies \
        x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Chrome is installed in the image so opening a new Codespace needs no setup.
RUN curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    -o /tmp/google-chrome.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends /tmp/google-chrome.deb \
    && rm -f /tmp/google-chrome.deb \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --break-system-packages --no-cache-dir websockets

USER vscode

RUN mkdir -p /home/vscode/.vnc \
    && printf '%s\n' \
        '#!/bin/sh' \
        'unset SESSION_MANAGER' \
        'unset DBUS_SESSION_BUS_ADDRESS' \
        'export XDG_CURRENT_DESKTOP=XFCE' \
        'export XDG_CONFIG_DIRS=/etc/xdg/xdg-xfce:/etc/xdg' \
        'startxfce4' \
        > /home/vscode/.vnc/xstartup \
    && chmod +x /home/vscode/.vnc/xstartup