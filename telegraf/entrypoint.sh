#!/bin/bash
set -e

# Configure auth
if [[ -z "${MQTT_USER}" || -z "${MQTT_PASSWORD}" ]]; then
  echo "Using un-authenticated configuration"
else
  echo "Configuring username/password authentication"
  sed -i -e 's/^  # username =.*/  username = \"'"${MQTT_USER}"'\"/g' -e 's/^  # password =.*/  password = \"'"${MQTT_PASSWORD}"'\"/g' /etc/telegraf/telegraf.d/*.conf
fi

if [ "${1:0:1}" = '-' ]; then
    set -- telegraf "$@"
fi

if [ $EUID -ne 0 ]; then
    exec "$@"
else
    # Allow telegraf to send ICMP packets and bind to privliged ports
    setcap cap_net_raw,cap_net_bind_service+ep /usr/bin/telegraf || echo "Failed to set additional capabilities on /usr/bin/telegraf"

    exec setpriv --reuid telegraf --init-groups "$@"
fi
