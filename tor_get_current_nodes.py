__date__ = "Nov 28, 2014"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import urllib2
import time
import sys

def get_tor_nodes(url):
    response = urllib2.urlopen(url)
    content = response.read()
    product_list=[]
    product_list += content.split("\n")
    return product_list


def syslog_cef(product_list,nodetype):
    for element in product_list:
        cef_exit_node = 'CEF:0|Tor Node|{0}|1.0|{0}|{0} Node|1| src={1}'.format(nodetype,element)
        # DEBUG:
        print cef_exit_node
        syslog.syslog(cef_exit_node)
    time.sleep(0.01)


def main():
    """
    Execute get_tor_nodes function every 24 hours
    :return: None
    """
    start_time = time.time()
    syslog_cef( get_tor_nodes( "http://torstatus.blutmagie.de/ip_list_exit.php" ), "Tor Exit" )
    syslog_cef( get_tor_nodes( "http://torstatus.blutmagie.de/ip_list_all.php" ), "Tor Router" )


if __name__ == "__main__":
  main()

