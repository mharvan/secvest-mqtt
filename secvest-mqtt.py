#!/usr/bin/python3

import config
import secvest
import paho.mqtt.publish as publish

s = secvest.Secvest(config.HOST, config.PORT, config.USER, config.PASSWD)
s.login()

print('### get_faults ###')
faults = s.get_faults()

print('### get_state_zones ###')
(state, zones) = s.get_state_zones()

s.logout()

# Process information
zones = set(zones)
faults = set(faults)
nonfaults = zones - faults
print('state:', state)
print('faults:', faults)
print('zones without faults:', nonfaults)


print('### mqtt publish ###')
msgs = []
msgs.append({'topic':'secvest/partition/1/state',
             'payload':state,
             'qos':0,
             'retain':config.RETAIN})
for zone in faults:
    msgs.append({'topic':'secvest/zone/%s/state' % zone,
                 'payload': 'OPEN',
                 'qos':0,
                 'retain':config.RETAIN})
for zone in nonfaults:
    msgs.append({'topic':'secvest/zone/%s/state' % zone,
                 'payload': 'CLOSED',
                 'qos':0,
                 'retain':config.RETAIN})
print('msgs: ', len(msgs))
publish.multiple(msgs, hostname=config.MQTTHOST)
