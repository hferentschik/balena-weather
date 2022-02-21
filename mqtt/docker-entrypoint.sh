#!/bin/ash
set -e

# Configure auth
if [[ -z "${MQTT_USER}" || -z "${MQTT_PASSWORD}" ]]; then
  echo "Using un-authenticated configuration"
else
  echo "Configruing username/password authentication"
  sed -i -e 's/^#password_file$/password_file \/mosquitto\/config\/passwd/g' -e 's/^allow_anonymous true$/allow_anonymous false/' /mosquitto/config/mosquitto.conf
  mosquitto_passwd -c -b /mosquitto/config/passwd "${MQTT_USER}"  "${MQTT_PASSWORD}"
fi

# Set permissions
user="$(id -u)"
if [ "$user" = '0' ]; then
        [ -d "/mosquitto" ] && chown -R mosquitto:mosquitto /mosquitto || true
fi

exec "$@"
