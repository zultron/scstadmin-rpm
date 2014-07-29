#!/bin/bash
#
# qla2x00t  
#
# chkconfig: 2345 14 86
# description: System startup script for the QLogic 22xx/23xx card target driver.
#
### BEGIN INIT INFO
# Provides:       qla2x00t
### END INIT INFO

. /etc/init.d/functions

RETVAL=0

KERNEL_MODULES="qla2x00t"

start() {
	echo -n $"Loading and configuring the QLogic target driver: "

	for module in ${KERNEL_MODULES}; do
		/sbin/modprobe "${module}" >/dev/null 2>&1
		RETVAL=$?
		[ $RETVAL != 0 ] && echo && return $RETVAL
	done

	echo
	return $RETVAL
	}

stop() {
	echo -n $"Stopping and unloading the QLogic target driver: "

	for module in ${KERNEL_MODULES}; do
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
	echo -n $"QLogic target driver status: "

	for module in ${KERNEL_MODULES}; do
		if [ ! -e "/sys/module/${module}" ]; then
                        RETVAL=3
                        echo
                        return $RETVAL
                fi
        done

        echo
        return $RETVAL
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
        status >/dev/null && restart
        ;;
    status)
	status
        ;;
    *)
        echo "Usage: $0 {start|stop|status|try-restart}"
        exit 2
        ;;
esac

exit $RETVAL 
