$file = "./irremote.ino"
$port = "COM4"
$baudrate = 115200
arduino-cli compile --fqbn arduino:avr:uno
arduino-cli upload --fqbn arduino:avr:uno -p $port $file 
arduino-cli monitor -p $port -c baudrate=$baudrate
