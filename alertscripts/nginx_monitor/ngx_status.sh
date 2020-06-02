#!/bin/bash

HOST="127.0.0.1"
PORT=80
function ping {
   /usr/bin/ps -ef | grep nginx |grep -v "grep" | wc -l
}

function active {
   /usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | grep Active | awk '{ print $3 }'
}

function accepts {
   /usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | awk '{ if(NR==3) print $1} '
}

function handled {
   /usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | awk '{ if(NR==3) print $2} '
}

function requests {
   /usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | awk '{ if(NR==3) print $3} '
}

function reading {
	/usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | grep Reading | awk '{ print $2 }'
}

function writing {
	/usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | grep Writing | awk '{ print $4 }' 
}

function waiting {
	/usr/bin/curl -s "http://$HOST:$PORT/nginx_status" 2>/dev/null | grep Waiting | awk '{ print $6 }' 
}
$1
