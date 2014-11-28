__date__ = "Dec 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import requests
from run_service.daemon_service import *
from syslog.syslog_tcp import *


def cull_csv_data(url_element, file_name):
    """Cull URL Data"""
    get_request_url = requests.get(url_element)
    if get_request_url.status_code == 200:
        data = get_request_url.text
        with open(file_name, 'wt') as f:
            f.write(data)


def tor_router_nodes():
    """Cull Tor Router Nodes"""
    SEARCH_BASE = "http://128.31.0.34:9031/tor/status/all"
    file_name = "tor_router_nodes.txt"
    cull_csv_data(SEARCH_BASE, file_name)
    open_file = open(file_name, 'rt')
    sock = syslog_tcp_open('127.0.0.1', port=1026)
    for i, line in enumerate(open_file):
        if line.startswith('r'):
            url_data_list = [str(i), line.split()[1:]]
            url_data_dict = dict(zip(url_data_list[0:5], url_data_list[1:]))
            for values in url_data_dict.values():
                try:
                    element = values[5].strip('\n')
                    cef_router_node = 'CEF:0|Tor Router Node|Tor Router|1.0|Router Node|Tor Router Node|1| dst=%s' % \
                                      element
                    syslog_tcp(sock, "%s" % cef_router_node, priority=0, facility=7)
                except ValueError:
                    return ValueError
    syslog_tcp_close(sock)


def tor_exit_nodes():
    """Cull Tor Exit Nodes"""
    url_list = ["http://exitlist.torproject.org/exit-addresses", "http://exitlist.torproject.org/exit-addresses.new"]
    sock = syslog_tcp_open('127.0.0.1', port=1026)
    for url_element in url_list:
        file_name = "tor_exit_nodes.txt"
        cull_csv_data(url_element, file_name)
        open_file = open(file_name, 'rt')
        for i, line in enumerate(open_file):
            if line.startswith('ExitAddress'):
                url_data_list = [str(i), line.split()[1:]]
                url_data_dict = dict(zip(url_data_list[0:5], url_data_list[1:]))
                for values in url_data_dict.values():
                    try:
                        element = values[0].strip('\n')
                        cef_exit_node = 'CEF:0|Tor Exit Node|Tor Exit|1.0|Exit Node|Tor Exit Node|1| src=%s' % \
                                        element
                        syslog_tcp(sock, "%s" % cef_exit_node, priority=0, facility=7)
                    except IndexError:
                        return None
    time.sleep(0.01)
    syslog_tcp_close(sock)


def main():
    """Cull Tor Indicators Every 24 Hours"""
    tor_router_nodes()
    tor_exit_nodes()
    time.sleep(86400)


class MyDaemon(Daemon):
    """Define main() to be daemon"""
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