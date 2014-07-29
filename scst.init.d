#!/bin/bash
#
# scst:
#
# chkconfig: 2345 13 87
# description: start/stop SCST core services
# config: /etc/scst.conf
### BEGIN INIT INFO
# Provides:       scst
### END INIT INFO

. /etc/init.d/functions

RETVAL=0

SCST_CFG=/etc/scst.conf

# Modules to load/unload.
#
# !!! DON'T ADD HERE TARGET DRIVERS, WHICH IMMEDIATELLY START ACCEPTING
# !!! NEW CONNECTIONS, BECAUSE AT THIS POINT ACCESS CONTROL HASN'T CONFIGURED
# !!! YET!
#
SCST_MODULES="scst scst_disk scst_vdisk"

# Return values according to LSB for all commands but status:
# 0 - success
# 1 - generic or unspecified error
# 2 - invalid or excess argument(s)
# 3 - unimplemented feature (e.g. "reload")
# 4 - insufficient privilege
# 5 - program is not installed
# 6 - program is not configured
# 7 - program is not running
#

[ -x /usr/sbin/scstadmin ] || exit 5
[ -f $SCST_CFG ]           || exit 6


start() {
	echo -n $"Loading and configuring the mid-level SCSI target SCST: "

	for module in ${SCST_MODULES}; do
		/sbin/modprobe "${module}" >/dev/null 2>&1
		RETVAL=$?
		[ $RETVAL != 0 ] && echo && return $RETVAL
	done

	/usr/sbin/scstadmin -config $SCST_CFG >/dev/null 2>&1
	RETVAL=$?
	echo 
	return $RETVAL
}


stop() {
	echo -n $"Stopping the mid-level SCSI target SCST: "

	reverse_list=""
	for module in ${SCST_MODULES}; do
		reverse_list="${module} ${reverse_list}"
	done

	for module in ${reverse_list}; do
		if [ -e "/sys/module/${module}" ]; then
 			/sbin/rmmod "${module}" >/dev/null 2>&1
			RETVAL=$?
	                [ $RETVAL != 0 ] && echo && return $RETVAL
		fi 
	done

	echo
	return $RETVAL
}


status() {
	echo -n $"Mid-level SCSI target SCST status: "

        for module in ${SCST_MODULES}; do
		if [ ! -e "/sys/module/${module}" ]; then
			RETVAL=3
			echo
			return $RETVAL
		fi
        done
	echo
	return $RETVAL 
}

try-restart() {
	status >/dev/null 2>&1 && restart
	}

reload() {
	echo -n $"Reloading mid-level SCSI target SCST configuration: "
	/usr/sbin/scstadmin -config $SCST_CFG >/dev/null 2>&1
	RETVAL=$?
	echo
	return $RETVAL
}

force-reload() {
	echo -n $"Reloading mid-level SCSI target SCST configuration: "
	/usr/sbin/scstadmin -config $SCST_CFG >/dev/null 2>&1
        RETVAL=$?
	[ $RETVAL = 0 ] && echo && return $RETVAL
	restart
}

case "$1" in
    start)
	start
        ;;
    stop)
	stop
        ;;
    restart)
        stop
        start
        ;;
    try-restart)
	try-restart
        ;;
    reload)
	reload
        ;;
    force-reload)
	force-reload
        ;;
    status)
	status
        ;;
    *)
        echo "Usage: scst {start|stop|status|try-restart|restart|force-reload|reload}"
        exit 2
        ;;
esac

exit $RETVAL
