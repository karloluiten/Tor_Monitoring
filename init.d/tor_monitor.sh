#!/bin/bash

#############################
# AUTHOR & LICENSING
#############################
# __date__ = "May 15, 2013"
# __author__ = "AlienOne"
# __copyright__ = "GPL"
# __credits__ = ["Justin Jessup"]
# __license__ = "GPL"
# __version__ = "1.0.0"
# __maintainer__ = "AlienOne"
# __email__ = "Justin@alienonesecurity.com"
# __status__ = "Production"
#############################


##############################
# BASH INITIALIZATION SCRIPT #
##############################


#############################
# INSTALLATION INSTRUCTIONS #
#############################


# Save file to $PATH
# /etc/init.d/tor_monitor.sh
# Make service executable
# chmod u+x /etc/init.d/tor_monitor.sh
# Enable the service to startup on system reboot
# /sbin/chkconfig twit_monitor.sh on
# Check that it is enabled chkconfig --list
# twit_trans_id.sh    0:off  1:off  2:off  3:on   4:off  5:on   6:off


case "$1" in
  start)
    echo "Starting server"
    # Start the daemon
    python /opt/tor_monitor/tor_get_current_router_nodes.py start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python /opt/twitter/tor_get_current_router_nodes.py stop
    ;;
  restart)
    echo "Restarting server"
    python /opt/twitter/tor_get_current_router_nodes.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/tor_monitor.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
