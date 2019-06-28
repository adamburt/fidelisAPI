# Overview
___
## Python library for Fidelis API commands

This repository contains libraries for use with Fidelis Cybersecurity technologies

*The libraries are developed outside of Fidelis and are not endorsed by Fidelis*
___
## General Use

Within the .py file are 3 classes:

- fidelisEndpoint
- fidelisThreatBridge
- fidelisNetwork

As they are named, they are used to access various API calls from each of the technologies. They are instantiated with differing options as outlined in the below *example*:

```python

import fidelisAPI

fep = fidelisAPI.fidelisEndpoint(<host>, <username>, <password>, <authMethod>, <ignoressl>)
fnw = fidelisAPI.fidelisNetwork(<host>, <username>, <password>, <uid>, <useuid>, <ignoressl>)
tb = fidelisAPI.fidelisThreatBridge(<host>, <usessl>, <ignoressl>, <apikey>)

fepAlerts = fep.getAlerts(None, None, None, None, None, None)
fnwAlerts = fnw.execute("aac_alerts", None)
tbFeeds = tb.lists(True, False)

```

For a description of each of the inputs for the instatiation, please see the relevant section below.

For a description of all the possible functions within each class, refer to the Fidelis API documentation and correlate with the functions in this library. They are similarly named.
___
## Fidelis Endpoint

Instatiation:
```python

fep = fidelisAPI.fidelisEndpoint(<host>, <username>, <password>, <authMethod>, <ignoressl>)

```

When instantiated, there are 6 inputs that are required:

- <host> - (*string*) This is the hostname or IP address of the Web UI Server
- <username> - (*string*) Username with the correct permissions to access API commands
- <password> - (*string*) Password for the username above
- <authMethod> - (*string*) Either "post" or "get" and determines how authentication is carried out
- <ignoressl> - (*boolean*) Either *True* or *False* and determines whether to ignore SSL errors
___
## Fidelis Network

Instatiation:

```python

fnw = fidelisAPI.fidelisNetwork(<host>, <username>, <password>, <useuid>, <ignoressl>)

```

When instantiated, there are 5 inputs that are required:

- <host> - (*string*) This is the hostname or IP address of the CommandPost
- <username> - (*string*) Username with the correct permissions to access API commands
- <password> - (*string*) Password for the username above
- <uid> - (*string*) If you already know your UID, you can use it in calls rather than username and password
- <useuid> - (*boolean*) Either *True* or *False* and determines whether to use a generated uid for queries after authentication
- <ignoressl> - (*boolean*) Either *True* or *False* and determines whether to ignore SSL errors
  
When **authenticating** for the first time, you can obtain your **unique uid** (until you change your password) through the following method (*as an example* - Required items are marked with an asterisk \*):

```python
import fidelisAPI

fnw = fidelisAPI.fidelisNetwork(<host>*, <username>*, <password>*, <uid>, <useuid>, <ignoressl>)

uid = fnw.showUID()

```
Instatiation of following fidelisNetwork classes can then be done by providing your UID into the first call (Required items are marked with an asterisk \*):

```python

fnw = fidelisAPI.fidelisNetwork(<host>*, None*, None*, <uid>*, True*, <ignoressl>)

```

___
## Fidelis ThreatBridge

Instatiation:

```python

tb = fidelisAPI.fidelisThreatBridge(<host>, <usessl>, <ignoressl>, <apikey>)`

```

When instantiated, there are 4 inputs that are required:

- <host> - (*string*) This is the hostname or IP address of the Web UI Server
- <usessl> - (*boolean*) Either *True* or *False* and determines whether to use `http://` or `https://` in queries
- <ignoressl> - (*boolean*) Either *True* or *False* and determines whether to ignore SSL errors
- <apikey> - (*string*) API Key used for authentication
___
# API Commands

Each API class has its set of own commands. Feel free to browse them and refer to the relevant Fidelis API documentation. Generally the function names closely represent the functions available through the official APIs. The **exception** here is for **Fidelis Network**.

This really only has 1 command that accepts varying *"queries"* as outlined in the API documentation. For example; the API documentation for 9.1 for Network states that to execute a command to show all alerts, one would have to call:

`https://<commandpost>/query/aac_alerts.cgi?user=<username>&pass=<password>&<param>=<value>&<param>=<value>&.....&<param>=<value>`

To make this easier (and not re-write ALL of the API commands) one simply places the cgi reference name in the call with the commands required:

```python
alerts = fnw.execute("aac_alerts", {<"param" : "value" pairs go in here in a dictionary>})
```

___
