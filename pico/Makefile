PORT=/dev/tty.usbmodem1101
BAUDRATE=115200
PROJECT=./printer

check: FORCE
	ls /dev/tty.usbmodem*

clear: FORCE
	rshell -b ${BAUDRATE} -p ${PORT} rm /pyboard/main.py /pyboard/thermal_printer.py

upload: FORCE
	rshell -b ${BAUDRATE} -p ${PORT} rsync ${PROJECT} /pyboard

download: FORCE
	rshell -b ${BAUDRATE} -p ${PORT} rsync /pyboard ${PROJECT}

rshell: FORCE
	rshell -b ${BAUDRATE} -p ${PORT}

repl: FORCE
	rshell -b ${BAUDRATE} -p ${PORT} repl

FORCE: ;
