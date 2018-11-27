#!/usr/bin/bash

#browser configuration with proxy server parameters
PORT=1080
HOSTNAME=ei-spark-m

export PORT=$PORT
export HOSTNAME=$HOSTNAME

/usr/bin/google-chrome --proxy-server="socks5://localhost:$PORT" \
	--user-data-dir=/tmp/$HOSTNAME
