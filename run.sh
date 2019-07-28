#!/bin/bash
#
# Run in an ednless loop querying the secvest server for status and publishing status in mqtt.
# Querying takes about 20s and we sleep 60s between status queries.
#

SLEEPTIME=60

# Activate venv
source paho-mqtt/bin/activate

export TIMEFORMAT='Elapsed time: %R s'
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

# Loop forever
while true
do
    echo -n "Starting at "
    date -Iseconds
    time python3 ./secvest-mqtt.py
    # Sleep 1m between invocations
    echo "Sleeping"
    sleep $SLEEPTIME
    echo
    echo
done
