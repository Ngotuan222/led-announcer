#!/bin/bash
# Auto-detect Headphones card
HEADPHONES_CARD=$(cat /proc/asound/cards | grep Headphones | head -1 | awk '{print $1}')
if [ -n "$HEADPHONES_CARD" ]; then
    sed -i "s/hw:[0-9],0/hw:$HEADPHONES_CARD,0/" /home/admin/led-announcer/config/settings.yaml
fi
