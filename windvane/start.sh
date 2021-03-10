#!/bin/bash

# Start sshd if we don't use the init system
if [[ "$START_SSHD" == "1" ]]; then
  /usr/sbin/sshd -p 22 &
fi

python3 windvane.py
