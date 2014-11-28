__date__ = "Nov 28, 2014"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import requests
from run_service.daemon_service import *
from syslog.syslog_tcp import *


def get_tor_nodes(urls_list):
    """
    Get get current lists of tor exit and router nodes
    :param urls_list: List of url strings
    :return: CEF formatted event output TCP syslog
    """
    sock = syslog_tcp_open('127.0.0.1', port=1026)
    for url in urls_list:
        get_request_url = requests.get(url)
        if get_request_url.status_code == 200:
            if 'exit' in url:
                data = get_request_url.text
                tor_exit_list = data.encode('utf-8').split('\n')
                for element in tor_exit_list:
                    cef_exit_node = 'CEF:0|Tor Exit Node|Tor Exit|1.0|Exit Node|Tor Exit Node|1| src=%s' % element
                    syslog_tcp(sock, "%s" % cef_exit_node, priority=0, facility=7)
            if 'all' in url:
                data = get_request_url.text
                tor_router_list = data.encode('utf-8').split('\n')
                for element in tor_router_list:
                    cef_router_node = 'CEF:0|Tor Router Node|Tor Router|1.0|Router Node|' \
                                      'Tor Router Node|1| dst=%s' % element
                    syslog_tcp(sock, "%s" % cef_router_node, priority=0, facility=7)
    time.sleep(0.01)
    syslog_tcp_close(sock)


def main():
    """
    Execute get_tor_nodes function every 24 hours
    :return: None
    """
    start_time = time.time()
    urls_list = ["http://torstatus.blutmagie.de/ip_list_exit.php",
                 "http://torstatus.blutmagie.de/ip_list_all.php"]
    while True:
        get_tor_nodes(urls_list)
        time.sleep(86400 - ((time.time() - start_time) % 86400))


class MyDaemon(Daemon):
    """
    Main instance run as daemon
    """
    def run(self):
        while True:
            main()
            time.sleep(0.01)


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/tor_monitor.pid')
    if len(sys.argv) == 2:
        print('{} {}'.format(sys.argv[0], sys.argv[1]))
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print('Correct syntax: ')
        print("Usage: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)