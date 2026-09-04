#!/bin/bash

export DISPLAY=:1

echo "Starting PulseAudio..."

pulseaudio --start

sleep 2

# Create virtual microphone only if it doesn't already exist
if ! pactl list short sources | grep -q 'vnc_microphone'; then
    pactl load-module module-pipe-source \
        source_name=vnc_microphone \
        file=/tmp/vnc-microphone.pcm \
        format=s16le \
        rate=16000 \
        channels=1
fi

pactl set-default-source vnc_microphone

echo "Starting TightVNC..."

if ! ss -lnt | grep -q ':5901 '; then
    tightvncserver :1 \
        -geometry 1280x720 \
        -depth 16
fi

sleep 2

# Disable XFCE compositing for better VNC performance
xfconf-query -c xfwm4 -p /general/use_compositing -s false 2>/dev/null || true

echo "Starting noVNC..."

if ! ss -lnt | grep -q ':6080 '; then
    nohup websockify \
        --web=/usr/share/novnc/ \
        6080 \
        localhost:5901 \
        > "$HOME/noVNC.log" 2>&1 &
fi

echo
echo "Desktop started."
echo "VNC:     localhost:5901"
echo "noVNC:   port 6080"
echo "Display: :1"
echo "Size:    1280x720"
echo "Color:   16-bit"
echo "Audio:   PulseAudio"

