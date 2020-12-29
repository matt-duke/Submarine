ARDUNIO_CLI=bin/arduino-cli
FQBN=arduino:avr:mega
PORT=/dev/ttyACM0

if [ -f "$ARDUNIO_CLI" ]; then
    echo "$ARDUNIO_CLI exists."
else
    echo "Setting up arduino-cli $FILE..."
    ./setup.sh
fi

$ARDUNIO_CLI compile --fqbn $FQBN runnning
$ARDUNIO_CLI upload -p $PORT --fqbn $FQBN running