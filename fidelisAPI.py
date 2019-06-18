import requests
import json
from datetime import datetime
import os
from urllib.parse import unquote
from urllib.parse import quote
from pprint import pprint

class fidelisThreatBridge:
    def __init__(self, fidelisEndpoint):
        self.fidelisEndpoint = fidelisEndpoint
        self.lastError = ""
        self.lastSuccess = ""
        now = datetime.now()
        self.threatBridgeURL = "{0}/threatbridge".format(self.fidelisEndpoint.baseURL)

    def createTBDataObject(self, data):
        if type(data) is not str and type(data) is not dict:
            self.lastError = "Unknown input provided in input"
            return {}
        feedData = {}
        if type(data) is dict:
            try:
                if not data["defaultAssessment"]:
                    self.lastError = "defaultAssessment is missing"
                    return {}
                if not data["defaultConfidence"]:
                    self.lastError = "defaultConfidence is missing"
                    return {}
                if not data["defaultSeverity"]:
                    self.lastError = "defaultSeverity is missing"
                    return {}
                if not data["description"]:
                    self.lastError = "description is missing"
                    return {}
                if not data["useWithProcessBlocking"]:
                    self.lastError = "useWithProcessBlocking is missing"
                    return {}
                if not data["fileName"]:
                    self.lastError = "fileName is missing"
                    return {}
                if not data["source"]:
                    self.lastError = "source is missing"
                    return {}
                if not data["fieldMappings"]:
                    self.lastError = "fieldMappings is missing"
                    return {}
                if not data["hasCsvHeaderRow"]:
                    self.lastError = "hasCsvHeaderRow is missing"
                    return {}
                if not data["importFormat"]:
                    self.lastError = "importFormat is missing"
                    return {}
                if not data["name"]:
                    self.lastError = "name is missing"
                    return {}
                if not data["updatingMethod"]:
                    self.lastError = "updateMethod is missing"
                    return {}
            except Exception as err:
                self.lastError = "Not enough parameters provided - {0}".format(err)
                return {}
            try:
                feedData["defaultAssessment"] = data["defaultAssessment"]
                feedData["defaultConfidence"] = data["defaultConfidence"]
                feedData["defaultSeverity"] = data["defaultSeverity"]
                feedData["description"] = data["description"]
                feedData["useWithProcessBlocking"] = data["useWithProcessBlocking"]
                feedData["fileName"] = data["fileName"]
                feedData["source"] = data["source"]
                feedData["fieldMappings"] = data["fieldMappings"]
                feedData["hasCsvHeaderRow"] = data["hasCsvHeaderRow"]
                feedData["importFormat"] = data["importFormat"]
                feedData["name"] = data["name"]
                feedData["updatingMethod"] = data["updatingMethod"]
            except Exception as err:
                self.lastError = "Not enough parameters in dictionary - {0}".format(err)
                return {}

        if type(data) is str:
            try:
                with open(data, "r") as jsonFile:
                    jsonData = json.load(jsonFile)
                    feedData["defaultAssessment"] = jsonData["defaultAssessment"]
                    feedData["defaultConfidence"] = jsonData["defaultConfidence"]
                    feedData["defaultSeverity"] = jsonData["defaultSeverity"]
                    feedData["description"] = jsonData["description"]
                    feedData["useWithProcessBlocking"] = jsonData["useWithProcessBlocking"]
                    feedData["fileName"] = jsonData["fileName"]
                    feedData["source"] = jsonData["source"]
                    feedData["fieldMappings"] = jsonData["fieldMappings"]
                    feedData["hasCsvHeaderRow"] = jsonData["hasCsvHeaderRow"]
                    feedData["importFormat"] = jsonData["importFormat"]
                    feedData["name"] = jsonData["name"]
                    feedData["updatingMethod"] = jsonData["updatingMethod"]
            except Exception as err:
                self.lastError = "Not enough parameters in dictionary - {0}".format(err)
                return {}
        return feedData

    def printData(self, feedData):
        print("Name: {0}".format(feedData["name"]))
        print("Description: {0}".format(feedData["description"]))
        print("Use with Process Blocking: {0}".format(feedData["description"]))
        print("File: {0}".format(feedData["fileName"]))
        print("Import Format: {0}".format(feedData["importFormat"]))
        print("Hash CSV header?: {0}".format(feedData["hasCsvHeaderRow"]))
        print("Default Assessment: {0}".format(feedData["defaultAssessment"]))
        print("Default Confidence: {0}".format(feedData["defaultConfidence"]))
        print("Default Severity: {0}".format(feedData["defaultSeverity"]))
        print("Source: {0}".format(feedData["source"]))
        print("Field Mappings: {0}".format(feedData["fieldMappings"]))
        print("Update method: {0}".format(feedData["updatingMethod"]))

    def addFeed(self, feedData):
        if not feedData["defaultAssessment"]:
            self.lastError = "No default assessment defined"
            return False
        if not feedData["defaultConfidence"]:
            self.lastError = "No default confidence defined"
            return False
        if not feedData["defaultSeverity"]:
            self.lastError = "No default severity defined"
            return False
        if not feedData["fileName"]:
            self.lastError = "No file name defined"
            return False
        if feedData["importFormat"] == "CSV" and len(feedData["fieldMappings"]) < 1:
            self.lastError = "No field mappings defined"
            return False
        if not feedData["importFormat"]:
            self.lastError = "No import format defined"
            return False
        if not feedData["name"]:
            self.lastError = "No name defined"
            return False
        if len(feedData["updatingMethod"]) < 1:
            self.lastError = "No updating method defined"
            return False
        url = "{0}/addFeed".format(self.threatBridgeURL)
        requests.packages.urllib3.disable_warnings()
        headers = self.fidelisEndpoint.headers
        bodyRequest = {"useWithProcessBlocking": feedData["useWithProcessBlocking"], "updatingMethod":feedData["updatingMethod"],"feedParserSettings":{},"hasCsvHeaderRow":feedData["hasCsvHeaderRow"],"fieldMappings":feedData["fieldMappings"],"name":feedData["name"],"description":feedData["description"],"fileName":feedData["fileName"],"defaultAssessment":feedData["defaultAssessment"],"defaultSeverity":feedData["defaultSeverity"],"defaultConfidence":feedData["defaultConfidence"],"importFormat":feedData["importFormat"]}
        try:
            r = requests.put(url, data = json.dumps(bodyRequest), headers = headers, verify=False)
        except Exception as err:
            self.lastError = err
            return False
        self.lastSuccess = "Added feed \"{0}\"".format(feedData["name"])
        return True

    def deleteFeed(self, feedName):
        feedNames = self.getFeeds()
        deleteID = ""
        for item in feedNames:
            if item["name"] == feedName:
                deleteID = item["id"]
        if len(deleteID) < 1:
            self.lastError = "The feed name \"{0}\" does not exist".format(feedName)
            return False

        url = "{0}/delete/{1}".format(self.threatBridgeURL, deleteID)
        requests.packages.urllib3.disable_warnings()
        headers = self.fidelisEndpoint.headers
        try:
            r = requests.delete(url, headers = headers, verify=False)
        except Exception as err:
            self.lastError = err
            return False
        if r.status_code == 200:
            self.lastSuccess = "Successfully deleted feed \"{0}\"".format(feedName)
            return True
        else:
            self.lastError = r.content
            return True

    def getFeeds(self):
        url = "{0}/feeds".format(self.threatBridgeURL)
        headers = self.fidelisEndpoint.headers
        requests.packages.urllib3.disable_warnings()
        try:
            r = requests.get(url, headers=headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return False
        returnedValues = []
        
        if not rData or rData == None or type(rData) != dict:
            return returnedValues
        try:
            if not rData["data"] and not rData["data"]["data"]:
                return returnedValues
        except:
            return returnedValues

        for feed in rData["data"]["data"]:
            returnedValues.append(feed)
        return returnedValues

    def searchFeeds(self, searchTerm, feedNames):
        url = "{0}/search/ungrouped".format(self.threatBridgeURL)
        requests.packages.urllib3.disable_warnings()
        headers = self.fidelisEndpoint.headers
        page = 0
        bodyRequest = {"collateResults": True,"ignoredAssessments": [],"ignoredDescriptions": [],"ignoredFeedSources": [],"ignoredSeverities": [],"indicesToExclude": ["accessdata_threatlookup"],"indicesToSearch": [],"orderAscending": True,"orderBy": "alternativeId","searchList": [{"firstResult": page,"indicesToSearch": [],"itemIdentifier": "","searchString": "*","searchType": "AllWildcard","uniqueSearchId": ""}],"trackPerformance": True}
        if feedNames and type(feedNames) is not list:
            self.lastError = "Please provide a list as the feedNames parameter. We got a {0}".format(type(feedNames))
            return []
        if searchTerm:
            bodyRequest["searchList"][0]["searchString"] = "*{0}*".format(searchTerm)
        if feedNames and type(feedNames) == list and len(feedNames) > 0:
            allFeeds = self.getFeeds()
            for item in feedNames:
                for feed in allFeeds:
                    if feed["name"] == item:
                        bodyRequest["indicesToSearch"].append(feed["id"])
        keepGoing = 1
        returnedData = []
        while keepGoing:
            try:
                r = requests.put(url, data = json.dumps(bodyRequest), headers = headers, verify=False)
                if type(r.content) == bytes:
                    rData = json.loads(r.content.decode("utf-8"))
                else:
                    rData = json.loads(r.content)
                keepGoing = rData["data"]["count"]
            except Exception as err:
                self.lastError = err
                return []
            if not rData["success"] == True:
                self.lastError = rData["error"]
                return []
            for intel in rData["data"]["data"]:
                returnedData.append(intel["threatDocument"])
            page = page + keepGoing
            bodyRequest["searchList"][0]["firstResult"] = page
        return returnedData

class fidelisEndpoint:

    def __init__(self, host, username, password):
        self.host = host
        self.baseURL = "https://{0}/endpoint/api".format(host)
        self.username = username
        self.password = password
        self.lastError = ""
        self.lastSuccess = ""
        self.checkURL = False
        self.ignoressl = True
        self.authToken = self.getAuthToken(self.username, self.password)
        self.headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "bearer {0}".format(self.authToken)}

    def getAuthToken(self, username, password):        
        url = "{0}/authenticate?username={1}&password={2}".format(self.baseURL, quote(username), quote(password))
        requests.packages.urllib3.disable_warnings()
        try:
            r = requests.get(url, verify=False)
        except Exception as err:
            self.lastError = "Error performing get request to URL- {0}".format(err)
            return None
        try:
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = "Error parsing JSON data returned from authentication URL - {0}".format(err)
            return None
        if (rData["success"] == False):
            self.lastError = "Error returned from authentication request - {0}".format(rData["error"]["message"])
            return None
        try:
            return rData["data"]["token"]
        except Exception as err:
            self.lastError = err
            return None

    def __findWithSearchCriteria__(self, url, searchCriteria, searchName):
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        if searchCriteria:
            url = "{0}&{1}={2}".format(url, searchName, searchCriteria)
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        try:
            if rData["success"] == False:
                self.lastError = rData["error"]
                return None
            return rData
        except Exception as err:
            self.lastError = err
            return None

    def getHostInfo(self):
        url = "{0}/product-info".format(self.baseURL)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        if rData["success"] == False:
            self.lastError = rData["error"]
            return None
        try:
            return rData["data"]
        except Exception as err:
            self.lastError = err
            return None

    def searchScripts(self, searchCriteria, limit):
        url = "{0}/playbooks/PlaybooksAndScripts?filterType=0&isManagementRequest=false&platformFilter=0&skip=0&sort=&take={1}".format(self.baseURL, limit)
        data = self.__findWithSearchCriteria__(url, searchCriteria, "search")
        try:
            return data["data"]["entities"]
        except Exception as err:
            self.lastError = err
            return None

    def getAllEndpoints(self, limit):
        if limit is None:
            limit = 1000000
        url = "{0}/endpoints/0/{1}/hostname".format(self.baseURL, limit)
        data = self.__findWithSearchCriteria__(url, None, None)
        return data

    def getEndpointDetails(self, endpointId):
        url = "{0}/endpoints/getEndpointDetailsExpanded/{1}".format(self.baseURL, endpointId)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        try:
            if rData["success"] == False:
                self.lastError = rData["error"]
                return None
            return rData["data"]
        except Exception as err:
            self.lastError = err
            return None
        try:
            return data
        except Exception as err:
            self.lastError = err
            return None

    def getEndpointFromHostname(self, hostname):
        endpoints = self.getAllEndpoints(1000000)
        thisEndpoint = None
        for endpoint in endpoints:
            if endpoint["hostName"].lower() == hostname.lower():
                thisEndpoint = endpoint
                break
        return thisEndpoint

    def searchEndpointSoftware(self, endpointID, searchCriteria, limit):
        url = "{0}/installedSoftware/{1}?skip=0&sort=installDate+Descending&take={2}".format(self.baseURL, endpointID, limit)
        data = self.__findWithSearchCriteria__(url, searchCriteria, "facetSearch")
        try:
            return data["data"]["entities"]
        except Exception as err:
            self.lastError = err
            return None

    def searchAlerts(self, searchCriteria, limit, startDate, endDate, sort):
        if sort is None:
            sort = "insertionDate+Descending"
        datenow = datetime.now()
        if endDate is None:
            endDate = datenow.strftime("%y-%m-%dT%H:%M:%S.000Z")
        if startDate is None:
            startDate = "1970-01-01T00:00:00.000Z"
        url = "{0}/alerts/getalerts?endDate={1}&startDate={2}&filterType=0&skip=0&sort={3}&take={4}".format(self.baseURL, endDate, startDate, sort, limit)
        data = self.__findWithSearchCriteria__(url, searchCriteria, "facetSearch")
        try:
            return data["data"]["entities"]
        except Exception as err:
            self.lastError = err
            return None

    def searchExecutables(self, searchCriteria, limit):
        url = "{0}/executables?skip=0&sort=reportingDate+Descending&take={1}".format(self.baseURL, limit)
        data = self.__findWithSearchCriteria__(url, searchCriteria, "facetSearch")
        try:
            return data["data"]["entities"]
        except Exception as err:
            self.lastError = err
            return None

    def searchSoftware(self, searchCriteria, limit):
        url = "{0}/installedSoftware?skip=0&sort=name+Ascending&take={1}".format(self.baseURL, limit)
        data = self.__findWithSearchCriteria__(url, searchCriteria, "facetSearch")
        try:
            return data["data"]["entities"]
        except Exception as err:
            self.lastError = err
            return None

    def recursiveGroupAdd(self, groupStructure, returnedData):
        try:
            returnedData.append({"name":groupStructure["name"], "id":groupStructure["id"]})
        except:
            return
        for child in groupStructure["children"]:
            self.recursiveGroupAdd(child, returnedData)

    def getGroups(self):
        url = "{0}/groups/GetGroupTree?includeAmAr=true&accessType=2".format(self.baseURL)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        if rData["success"] == False:
            self.lastError = rData["error"]
            return None
        try:
            return rData["data"]
        except Exception as err:
            self.lastError = err
            return None

    def getGroupName(self, groupID):
        allGroups = self.getGroups()
        allData = []
        self.recursiveGroupAdd(allGroups, allData)
        returnedItems = ""
        for item in allData:
            if item["id"].lower() == groupID.lower():
                returnedItems  = item["name"]
        try:
            return returnedItems
        except Exception as err:
            self.lastError = err
            return None

    def getGroupID(self, groupName, contains):
        allGroups = self.getGroups()
        allData = []
        self.recursiveGroupAdd(allGroups, allData)
        returnedItems = None
        for item in allData:
            if contains:
                if returnedItems is None:
                    returnedItems = []
                if item["name"].lower().find(groupName.lower()) != -1:
                    returnedItems.append(item["id"])
            if not contains:
                if returnedItems is None:
                    returnedItems = []
                if item["name"] == groupName:
                    returnedItems.append(item["id"])
        try:
            return returnedItems
        except Exception as err:
            self.lastError = err
            return None

    def getGroupEndpoints(self, groupName):
        allEndpoints = self.getAllEndpoints(None)
        if allEndpoints is None:
            return None
        if allEndpoints["success"]:
            allEndpoints = allEndpoints["data"]["endpoints"]
        else:
            return None
        returnedEndpoints = []
        partialList = []
        for endpoint in allEndpoints:
            try:
                groupList = endpoint["groupList"].split("\n")
                if groupName in groupList:
                    partialList.append(endpoint)
            except:
                pass
        for partialEndpoint in partialList:
            thisExists = False
            for returnedEndpoint in returnedEndpoints:
                if returnedEndpoint["hostName"] == partialEndpoint["hostName"]:
                    thisExists = True
                    break
            if not thisExists:
                returnedEndpoints.append(partialEndpoint)            
        return returnedEndpoints

    def executeScript(self, scriptID, endpoints, groups):
        url = "{0}/scriptPackages/scriptPackage/{1}".format(self.baseURL, scriptID)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        playbook = False
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        if rData["success"] == False:
            if rData["error"]["statusCode"] == 500 and rData["error"]["message"] == "Sequence contains no elements":
                url = "{0}/playbooks/PlaybookDetail?id={1}".format(self.baseURL, scriptID)
                try:
                    r = requests.get(url, headers = headers, verify=False)
                    if type(r.content) == bytes:
                        rData = json.loads(r.content.decode("utf-8"))
                    else:
                        rData = json.loads(r.content)
                    
                    if rData["success"] == True:
                        playbook = True
                except Exception as err:
                    self.lastError = err
                    return None
        jsonData = rData["data"]
        endpointsList = []
        for group in groups:
            theseGroupIDs = self.getGroupID(group, False)
            for groupID in theseGroupIDs:
                allGroupEndpoints = self.getGroupEndpoints(groupID)
                for endpoint in allGroupEndpoints:
                    endpointsList.append(endpoint["id"])
        allEndpoints = self.searchEndpoints(None)
        allIDs = []
        for endpoint in allEndpoints:
            for endpointName in endpoints:
                if endpoint["hostName"] == endpointName:
                    if endpoint["id"] not in allIDs:
                        allIDs.append(endpoint["id"])
        
        for thisID in allIDs:
            if thisID not in endpointsList:
                endpointsList.append(thisID)
                        
        returnedData = ""
        url = "{0}/jobs/createTask".format(self.baseURL)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        bodyRequest = {"packageId": jsonData["id"], "isPlaybook": playbook, "endpoints": endpointsList}
        if playbook:
            bodyRequest["taskOptions"] = jsonData["scripts"]
            for item in bodyRequest["taskOptions"]:
                del item["integrationOutputFormat"]
        if not playbook:
            bodyRequest["taskOptions"] = [{"detailsLoaded": False, "questions": jsonData["questions"], "queueExpirationInhours": 0, "scriptId": jsonData["id"], "timeoutInSeconds": jsonData["timeoutSeconds"], "details":jsonData}]
        try:
            r = requests.post(url, data = json.dumps(bodyRequest), headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        if rData["success"] == False:
            self.lastError = rData["error"]
            return None
        if rData["success"] == True:
            self.lastSuccess = "Script executed with ID {0}".format(rData["data"])
            try:
                return rData["data"]
            except Exception as err:
                self.lastError = err
                return None

    def getJobStatus(self, jobID):
        url = "{0}/jobs/getjobResult/{1}".format(self.baseURL, jobID)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        if rData["success"] == False:
            self.lastError = rData["error"]
            return None
        try:
            return rData
        except Exception as err:
            self.lastError = err
            return None

    def searchEvents(self, searchCriteria, limit):
        url = "{0}/v2/events?pageSize={1}".format(self.baseURL, limit)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.post(url, headers = headers, data = json.dumps(searchCriteria), verify=False)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("UTF-8"))
            else:
                rData = json.loads(r.content)
        except Exception as err:
            self.lastError = err
            return None
        try:
            if rData["success"] == False:
                self.lastError = rData["error"]
                return None
            try:
                return rData["data"]["events"]
            except Exception as err:
                self.lastError = err
                return None
        except Exception as err:
            self.lastError = err
            return None

class fidelisNetwork:
    def __init__(self, host, username, password):
        self.lastError = ""
        self.lastSuccess = ""
        self.host = host
        self.username = username
        self.password = password
        self.headers = {"Content-Type": "text/tab-separated-summary-urlencode-values"}
        self.baseURL = "https://{0}/query/<cgi_name>.cgi?user={1}&pass={2}".format(self.host, self.username, self.password)

    def __findWithSearchCriteria__(self, url, searchCriteria, limit):
        url = "{0}&amount={1}".format(url, limit)
        requests.packages.urllib3.disable_warnings()
        headers = self.headers
        if searchCriteria and len(searchCriteria) > 0:
            url = "{0}&{1}".format(url, searchCriteria)
        try:
            r = requests.get(url, headers = headers, verify=False)
        except Exception as err:
            self.lastError = err
            return None
        returnedData = {"data":[], "lowestID":0, "highestID":0, "count":0}
        raw = r.content.decode("utf-8")
        raw = unquote(raw)
        rawLines = raw.splitlines()
        headers = rawLines[0].split("\t")
        rawLines.remove(rawLines[0])
        for line in rawLines:
            line = line.split("\t")
            dataItem = {}
            for x in range(len(line)):
                dataItem[headers[x]] = line[x]
            returnedData["data"].append(dataItem)
            returnedData["count"] = returnedData["count"] + 1
        returnedData["highestID"] = int(returnedData["data"][0]["alertID"])
        returnedData["lowestID"] = int(returnedData["data"][-1]["alertID"])
        return returnedData


    def searchAlerts(self, searchCriteria, limit):
        url = self.baseURL.replace("<cgi_name>", "aac_alerts")
        data = self.__findWithSearchCriteria__(url, searchCriteria, limit)
        return data
        
