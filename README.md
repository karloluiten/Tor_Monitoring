###Tor Router & Exit Node Monitoring - ArcSight Use Case 

####Data Sources
- http://torstatus.blutmagie.de/ip_list_exit.php
- http://torstatus.blutmagie.de/ip_list_all.php

####Use Case Description
Harvest actively recorded Tor router and exit nodes. Tor anonymous routing services are often
utilized by nefarious actors to conduct hacking operations against customers information systems infrastructure.
Strategy is to daily update Active Lists within ArcSight SIEM in an effort to monitor and alert on any
customer assets that may communicate with any known Tor router nodes. Additionally monitor and alert on any
Tor Exit nodes that may communicate with the customer's information systems infrastructure.

####Collection & Processing Methodology 
- Harvest Tor router and exit node data from data sources monitoring and updating on said registration of Tor assets.

####Culled Attribute to ArcSight Mappings
**Python Object - ArcSight Schema Field - Description**
element - SourceAddress - None 

**ArcSight CEF Mappings - Assignment - Description if Any**
- SourceAddress - Tor Router/Exit Node - None
- DeviceProduct => Tor Router Node/Tor Exit Node - None
- DeviceVendor => Tor Exit Node/Tor Router Node - None
- DeviceEventClassID => Exit Node/Router Node - None

####ArcSight Content Development
- Create Real Time Rule to populate Active List 
- Active List Composed of IPAddress - String
- String assignment should be DeviceEventClassID
- Create Real Time Rule to monitor outbound communications of customer assets with Tor Router Nodes 
- Create Real Time Rule to monitor inbound communications of customer assets SourceAddress

####Long Term Deployment 
- Implementation runs as a daemon process on system
- Main function is executed every 24 hours to update lists

####TODO
- None at this point in time
