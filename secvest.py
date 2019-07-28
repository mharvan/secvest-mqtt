import json
import logging
import requests
import traceback
from bs4 import BeautifulSoup as bs
from datetime import datetime
from xml.etree import ElementTree as ET

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)

class Secvest():
    def __init__(self, host, port, user, passwd):
        self.URLBASE = "https://%s:%d/" % (host, port)
        self.user = user
        self.passwd = passwd
        self.ssid = None
        self.cookies = {}

    def login(self):
        """Login into Secvest system to start a session and obtain an ssid."""
        try:
            logger.debug("Logging in")
            url = self.URLBASE + 'sec_login.cgi'
            data = {
                'usr': self.user,
                'pwd': self.passwd
            }
            resp = requests.post(url, data=data, verify=False)

            logger.debug('Login request response status code: %d' % resp.status_code)
            if resp.status_code != 200:
                logger.error("Login failed with non-200 response code")

            # Extract ssid
            soup = bs(resp.text, 'html.parser')
            ssid = soup.find('input',{'id':'ssid'})['value']
            logger.debug('Login failed, ssid:', ssid)
            if (ssid == '0'):
                logger.error("Login failed")
                return False
            else:
                self.cookies = { 'ssid': ssid }
                return True
        except:
            print('Exception')
            traceback.print_exc()

    def logout(self):
        """Logout to end current session."""
        try:
            url = self.URLBASE + 'index.htm'
            data = {'ssid': '',
                    'logout': 'logout'}
            logger.debug("Logging out")
            resp = requests.post(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('Logout request response status code: %d' % resp.status_code)
        except:
            print('Exception')
            traceback.print_exc()

    def get_state_zones(self, partition=1):
        """Request partition info.

        Includes partitions status (set, unset, partset) and list of zones included in partition.
        
        Returns tuple (state, zones) where
        * state is a string set/partset/unset
        * zones is a list of zones assigned to partition
        """
        try:
            url = self.URLBASE + ('system/partition-%d/zone' % partition)
            dt = datetime.now()
            data={'_': dt.microsecond}
            logger.debug("Requesting partition 1 zones")
            resp = requests.get(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('Request response status code: %d' % resp.status_code)
            """Example response:
        {
            "id": "1",
            "name": "Partition 1",
            "state": "unset",
            "zones" : [
                "201",
                "202",
                "203",
                "204",
                "205",
                "206",
                "207",
                "208",
                "209",
                "210",
                "211",
                "212",
                "213",
                "214",
                "215",
                "216",
                "217",
                "218",
                "219"
            ]
        }        
"""
            #print('Response text:', resp.text)
            #return resp.json()
            d = resp.json()
            state = d['state']
            zones = d['zones']
            return (state, zones)
        except:
            print('Exception')
            traceback.print_exc()

    def get_faults(self):
        """Get list of faults (open zones).

        Returns list of open zones (IDs, not user-friendly names).
        Note: API response includes also user-frienfly zone names.
        """
        try:
            url = self.URLBASE + 'faults/'
            dt = datetime.now()
            data={'_': dt.microsecond}
            resp = requests.get(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('Faults request response status code: %d' % resp.status_code)
            #print('Response text:', resp.text)
            """
        Example response:
[
    {
        "type": "5000",
        "id": "1288",
        "ui-string": "Z207 A Do Kitchen",
        "affects-partition" : [
            "1"
        ],
        "affects-zone": "207",
        "prevents-set": true,
        "prevents-reset": false,
        "is-rf-warning": false
    },
    {
        "type": "5000",
        "id": "1292",
        "ui-string": "Z211 A Wi Bathroom",
        "affects-partition" : [
            "1"
        ],
        "affects-zone": "211",
        "prevents-set": true,
        "prevents-reset": false,
        "is-rf-warning": false
    },
    {
        "type": "5000",
        "id": "1294",
        "ui-string": "Z213 A Wi Bedroom",
        "affects-partition" : [
            "1"
        ],
        "affects-zone": "213",
        "prevents-set": true,
        "prevents-reset": false,
        "is-rf-warning": false
    }
]
            """
            d = resp.json()
            faults = map(lambda x: x['affects-zone'], d)
            return faults
        except:
            print('Exception')
            traceback.print_exc()


    def __parse_sec_global_status(self, str):
        """Parse response to GET /sec_global_status."""
        tree = ET.fromstring(str)
        open_zones = map(lambda p: p.find('name').text,
                         tree.findall('.//open_zones/zone'))
        return open_zones

    def get_global_status(self):
        """Request global status"""
        try:
            url = self.URLBASE + 'sec_global_status.cgx'
            dt = datetime.now()
            data={'_': dt.microsecond}
            logger.debug("Requesting global status (open zones)")
            resp = requests.get(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('Sec global status request response code: %d' % resp.status_code)
            open_zones = self.__parse_sec_global_status(resp.text)

            print("Open zones:")
            for oz in open_zones:
                print('   ' + oz)
        except:
            print('Exception')
            traceback.print_exc()

    def get_state_zones(self, partition=1):
        """Request partition info.

        Includes partitions status (set, unset, partset) and list of zones included in partition.
        
        Returns tuple (state, zones) where
        * state is a string set/partset/unset
        * zones is a list of zones assigned to partition
        """
        try:
            url = self.URLBASE + ('system/partition-%d/zone' % partition)
            dt = datetime.now()
            data={'_': dt.microsecond}
            logger.debug("Requesting partition 1 zones")
            resp = requests.get(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('Request response status code: %d' % resp.status_code)
            """Example response:
        {
            "id": "1",
            "name": "Partition 1",
            "state": "unset",
            "zones" : [
                "201",
                "202",
                "203",
                "204",
                "205",
                "206",
                "207",
                "208",
                "209",
                "210",
                "211",
                "212",
                "213",
                "214",
                "215",
                "216",
                "217",
                "218",
                "219"
            ]
        }        
"""
            #print('Response text:', resp.text)
            #return resp.json()
            d = resp.json()
            state = d['state']
            zones = d['zones']
            return (state, zones)
        except:
            print('Exception')
            traceback.print_exc()

    # TODO: Not working yet
    def set_state(self, state, partition=1):
        """Set state of partition (set/partset/unset)."""

        if (state not in ['set', 'partset', 'unset']):
            logger.error('Desired partition state must be one of set, partset, unset')

        try:
            url = self.URLBASE + ('system/partitions-%d/' % partition)
            data={'state': state}
            resp = requests.put(url, data=data, cookies=self.cookies, verify=False)
            logger.debug('State set request response status code: %d' % resp.status_code)
            print('Response code:', resp.status_code)
            print('Response text:', resp.text)
            return True
        except:
            print('Exception')
            traceback.print_exc()


# # Parse response to GET /system/partitions
# def parse_partitions_str(str):
#     data = json.loads(str)
#     return parse_partitions_json(data)

# # Rerturn state of Parittion 1:
# # * set
# # * unset
# # * partset
# # On error, returns the string unknown.
# def parse_partitions_json(data):
#     for p in data:
#         if (p['name'] == 'Partition 1'):
#             return p['state']
#     return 'unkown'


# # Request partitions
# try:
#     url = URLBASE + 'system/partitions/'
#     dt = datetime.now()
#     data={'_': dt.microsecond}
#     print()
#     logger.debug("Requesting partitions status")
#     resp = requests.get(url, data=data, cookies=cookies, verify=False)
#     logger.debug('code:', resp.status_code)
#     #print('response:', resp.text)
#     status = parse_partitions_json(resp.json())
#     logger.debug('status:', status)
# except:
#     print('Exception')
#     traceback.print_exc()


# TODO: Walktest to get user-friendly names of zones
