#! /bin/sh
### BEGIN INIT INFO
# Provides:          <run riotdb>
# Required-Start:    $all
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Manage my cool stuff
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/bin

. /lib/init/vars.sh
. /lib/lsb/init-functions
# If you need to source some other scripts, do it here

case "$1" in
  start)
    log_begin_msg "Starting my super cool service"
    sudo ifconfig eth0 192.168.1.2 netmask 255.255.255.0 up
    sudo python /home/pi/Documents/cesar/newParser.py

# do something
    log_end_msg $?
    exit 0
    ;;
  stop)
    log_begin_msg "Stopping the coolest service ever unfortunately"
    # do something to kill the service or cleanup or nothing
    log_end_msg $?
    exit 0
    ;;
  *)
    echo "Usage: /etc/init.d/<your script> {start|stop}"
    exit 1
    ;;
esac