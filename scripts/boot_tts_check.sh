#!/usr/bin/env bash
# Wait a bit to ensure service is ready
sleep 5
curl -X POST http://localhost:8000/announce \
  -u admin:hkqt@2024 \
  -H "Content-Type: application/json" \
  -d '{"fullname":"Hệ thống đã được khởi động"}' \
  >> /tmp/led-announcer-boot-check.log 2>&1 || true