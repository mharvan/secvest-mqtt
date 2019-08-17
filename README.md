# secvest-mqtt
Expose ABUS secvest via mqtt to integrate with openhab

## Update with walktest

In order to get a full listing of faults (open doors, windows,...) we
have to use GET /sec_global_status.cgx. This return only
human-friendly names of zones. We obtain the mapping between zone
codes and human-friendly names from walktest.