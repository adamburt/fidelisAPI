import requests
import json
from datetime import datetime
from urllib.parse import unquote
from urllib.parse import quote
import io

class fidelisEndpoint:

    def __init__(self, host, username, password, authMethod, ignoressl):
        self.host = host
        self.baseURL = "https://{0}/endpoint/api".format(host)
        self.username = username
        self.password = password
        self.ignoressl = ignoressl
        if self.ignoressl:
            self.checkURL = False
        else:
            self.checkURL = True
        self.lastError = None
        self.authToken = self.getAuthToken(self.username, self.password, authMethod)
        self.headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "bearer {0}".format(self.authToken)}     

    def getAuthToken(self, username, password, method):
        
        #Find out whether get is used rather than post
        useGet = False
        url = "{0}/authenticate".format(self.baseURL)
        if method.lower() == "get":
            url += "?username={0}&password={1}".format(quote(username), quote(password))
            useGet = True
        
        #Ignore SSL errors if specified
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        if useGet:
            try:
                r = requests.get(url, verify=self.checkURL)
            except Exception as err:
                self.lastError = "Error performing get request to URL- {0}".format(err)
                return None
        if not useGet:
            try:
                headers = {"Content-Type": "application/json"}
                bodyRequest = {"username": username, "password": password}
                r = requests.post(url, data = json.dumps(bodyRequest), headers = headers, verify=self.checkURL)
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
        if not rData["success"]:
            self.lastError = "Error returned from authentication request - {0}".format(rData["error"]["message"])
            return None
        try:
            return rData["data"]["token"]
        except Exception as err:
            self.lastError = err
            return None

    def __genericGetRequest__(self, url):
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def __genericPostRequest__(self, url, data):
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.post(url, headers = headers, data = json.dumps(data), verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def __genericDeleteRequest__(self, url, data):
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            if data:
                r = requests.delete(url, headers = headers, data = json.dumps(data), verify=self.checkURL)
            else:
                r = requests.delete(url, headers = headers, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def getAlertRules(self, limit, offset, sort, search):
        url = "{0}/alertrules".format(self.baseURL)

        if limit:
            if "?" not in url:
                url += "?limit={0}".format(limit)
            else:
                url += "&limit={0}".format(limit)
        if offset:
            if "?" not in url:
                url += "?offset={0}".format(offset)
            else:
                url += "&offset={0}".format(offset)
        if sort:
            if "?" not in url:
                url += "?sort={0}".format(sort)
            else:
                url += "&sort={0}".format(sort)
        if search:
            if "?" not in url:
                url += "?search={0}".format(json.dumps(search))
            else:
                url += "&search={0}".format(json.dumps(search))

        data = self.__genericGetRequest__(url, None, None)
        return data

    def createAlertRule(self, data):
        url = "{0}/alertrules".format(self.baseURL)
        rData = self.__genericPostRequest__(url, data)
        return rData

    def deleteAlertRules(self, data):
        url = "{0}/alertrules/delete".format(self.baseURL)
        rData = self.__genericPostRequest__(url, data)
        return rData

    def getAlerts(self, skip, take, sort, facetSearch, startDate, endDate):
        
        url = "{0}/alerts/getalerts".format(self.baseURL)
        if skip:
            if "?" not in url:
                url += "?skip={0}".format(skip)
            else:
                url += "&skip={0}".format(skip)
        if take:
            if "?" not in url:
                url += "?take={0}".format(take)
            else:
                url += "&take={0}".format(take)
        if sort:
            if "?" not in url:
                url += "?sort={0}".format(sort)
            else:
                url += "&sort={0}".format(sort)
        if facetSearch:
            if "?" not in url:
                url += "?facetSearch={0}".format(quote(facetSearch))
            else:
                url += "&facetSearch={0}".format(quote(facetSearch))
        if startDate:
            if "?" not in url:
                url += "?startDate={0}".format(quote(startDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            else:
                url += "&startDate={0}".format(quote(startDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
        if endDate:
            if "?" not in url:
                url += "?endDate={0}".format(quote(endDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
            else:
                url += "&endDate={0}".format(quote(endDate.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
        rData = self.__genericGetRequest__(url)
        return rData

    def getEndpoints(self, startIndex, count, sort):
        url = "{0}/endpoints".format(self.baseURL)
        if startIndex:
            url += "/{0}".format(startIndex)
        else:
            url += "/0"
        if count:
            url += "/{0}".format(count)
        else:
            url += "/10"
        if sort:
            url += "/{0}".format(sort)
        else:
            url += "/hostName"
        rData = self.__genericGetRequest__(url)
        return rData

    def getEndpointIdsbyEndpointNames(self, names):
        url = "{0}/endpoints/endpointidsbyname".format(self.baseURL)
        rData = self.__genericPostRequest__(url, names)
        return rData

    def deleteEndpoint(self, inputId):
        url = "{0}/endpoints/delete/{1}".format(self.baseURL, inputId)
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def getEvents(self, searchCriteria, pageSize):
        url = "{0}/v2/events".format(self.baseURL)
        if pageSize:
            url += "?pageSize={0}".format(pageSize)
        rData = self.__genericPostRequest__(url, searchCriteria)
        return rData

    def getEventCount(self, searchCriteria):
        url = "{0}/events/count".format(self.baseURL)
        rData = self.__genericPostRequest__(url, searchCriteria)
        return rData

    def fileSearch(self, searchCriteria):
        url = "{0}/files/search".format(self.baseURL)
        rData = self.__genericPostRequest__(url, searchCriteria)
        return rData

    def fileSearchJobStatus(self, jobId, jobResultId):
        url = "{0}/jobs/getjobstatus/{1}/{2}".format(self.baseURL, jobId, jobResultId)
        rData = self.__genericGetRequest__(url)
        return rData

    def fileSearchJobResults(self, jobId, jobResultId):
        url = "{0}/jobs/{1}/jobresults/{2}".format(self.baseURL, jobId, jobResultId)
        rData = self.__genericGetRequest__(url)
        return rData

    def fileSearchGetStream(self, fileId):
        url = "{0}/files/{1}".format(self.baseURL, fileId)
        
        #Copy our headers and remove the Content-Type
        headers = {}
        for k in self.headers:
            headers[k] = self.headers[k]
        del headers["Content-Type"]
        
        #Create a byte stream to copy the data into
        data = io.BytesIO()
        try:
            with requests.get(url, headers = headers, verify=self.checkURL, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024):
                    data.write(chunk)
        except Exception as err:
            return None
        return data.getvalue()

    def deleteJob(self, jobId):
        url = "{0}/jobs/{1}".format(self.baseURL, jobId)
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def getEndpointByIP(self, ip):
        url = "{0}/endpoints/search".format(self.baseURL)
        searchCriteria = {"ip": ip}
        rData = self.__genericPostRequest__(url, searchCriteria)
        return rData

    def getProductInfo(self):
        url = "{0}/product-info".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def getScriptPackages(self):
        url = "{0}/packages".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def getScriptPackageFile(self, scriptPackageId):
        url = "{0}/packages/{1}?type=File".format(self.baseURL, scriptPackageId)
        
        #Copy our headers and remove the Content-Type
        headers = {}
        for k in self.headers:
            headers[k] = self.headers[k]
        del headers["Content-Type"]
        
        #Create a byte stream to copy the data into
        data = io.BytesIO()
        try:
            with requests.get(url, headers = headers, verify=self.checkURL, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024):
                    data.write(chunk)
        except Exception as err:
            return None
        return data.getvalue()

    def getScriptPackageManifest(self, scriptPackageId):
        url = "{0}/packages/{1}?type=Manifest".format(self.baseURL, scriptPackageId)
        rData = self.__genericGetRequest__(url)
        return rData

    def getScriptPackageMetadata(self, scriptPackageId):
        url = "{0}/packages/{1}?type=Metadata".format(self.baseURL, scriptPackageId)
        rData = self.__genericGetRequest__(url)
        return rData

    def getScriptPackageTemplate(self, scriptPackageId):
        url = "{0}/packages/{1}?type=Template".format(self.baseURL, scriptPackageId)
        rData = self.__genericGetRequest__(url)
        return rData

    def executeScriptPackage(self, scriptCriteria):
        url = "{0}/packages/{1}/execute".format(self.baseURL, scriptCriteria["scriptPackageId"])
        rData = self.__genericPostRequest__(url, scriptCriteria)
        return rData

    def getScriptJobResults(self, jobResultId):
        url = "{0}/jobresults/scriptjob_{1}".format(self.baseURL, jobResultId)
        rData = self.__genericPostRequest__(url, None)
        return rData

    def getScriptJobTargets(self, jobResultId):
        url = "{0}/jobs/getjobtargets/{1}".format(self.baseURL, jobResultId)
        rData = self.__genericGetRequest__(url)
        return rData

    def createScriptPackage(self, scriptOptions):
        url = "{0}/scriptPackages/createUpdate".format(self.baseURL)
        rData = self.__genericPostRequest__(url, scriptOptions)
        return rData

    def uploadScriptPackageFiles(self, scriptPackageId, fileData):

        ##########################################################################################
        # fileData must be a JSON dictionary containing the files to upload with their names
        # For example: fileData = {"test.txt": open("C:\\test.txt", "rb")}
        ##########################################################################################

        url = "{0}/scriptPackages/scriptPackageFileUpload/{1}".format(self.baseURL, scriptPackageId)
        #Copy our headers and change the Content-Type
        headers = {}
        for k in self.headers:
            headers[k] = self.headers[k]
        del headers["Content-Type"]# = "multipart/form-data"

        #Ignore SSL errors?
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()

        #Make the request
        try:
            r = requests.post(url, headers = headers, files = fileData, data = None, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def finalizeScriptPackage(self, scriptPackageId):
        url = "{0}/scriptPackages/PackageChangeComplete/{1}/false".format(self.baseURL, scriptPackageId)
        rData = self.__genericPostRequest__(url, [])
        return rData

class fidelisThreatBridge:

    def __init__(self, ip, port, useSSL, ignoressl, apiKey):
        if useSSL:
            protocol = "https"
        else:
            protocol = "http"
        self.apiKey = apiKey
        self.baseURL = "{0}://{1}:{2}/ThreatBridgeService".format(protocol, ip, port)
        self.headers = None
        self.ignoressl = ignoressl
        if self.ignoressl:
            self.checkURL = False
        else:
            self.checkURL = True
        self.lastError = ""

    def __genericGetRequest__(self, url):
        if "?" in url:
            url += "&apiKey={0}".format(self.apiKey)
        else:
            url += "?apiKey={0}".format(self.apiKey)
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.get(url, headers = headers, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def __genericDeleteRequest__(self, url, data):
        if "?" in url:
            url += "&apiKey={0}".format(self.apiKey)
        else:
            url += "?apiKey={0}".format(self.apiKey)
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            if data:
                r = requests.delete(url, headers = headers, data = json.dumps(data), verify=self.checkURL)
            else:
                r = requests.delete(url, headers = headers, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def __genericPostRequest__(self, url, data):
        if "?" in url:
            url += "&apiKey={0}".format(self.apiKey)
        else:
            url += "?apiKey={0}".format(self.apiKey)
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.post(url, headers = headers, data = json.dumps(data), verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def __genericPutRequest__(self, url, data):
        if "?" in url:
            url += "&apiKey={0}".format(self.apiKey)
        else:
            url += "?apiKey={0}".format(self.apiKey)
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
            r = requests.put(url, headers = headers, data = json.dumps(data), verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def getProductInfo(self):
        url = "{0}/About".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def count(self, listId, threatListsOnly):

        ##########################################
        # listId = string
        # threatListOnly = boolean
        ##########################################

        url = "{0}/Count".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def globalStats(self, resetDaily, resetTotal):

        ##########################################
        # resetDaily = boolean
        # resetTotal = boolean
        ##########################################

        url = "{0}/GlobalStats".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def hello(self):
        url = "{0}/Hello".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def help(self, apiName, showParameters):

        ##########################################
        # apiName = string
        # showParameters = boolean
        ##########################################

        url = "{0}/Help".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def isAlive(self):

        url = "{0}/IsAlive".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def isBusy(self):

        url = "{0}/IsBusy".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def options(self, threatListsOnly):

        ##########################################
        # threatListsOnly = boolean
        ##########################################

        url = "{0}/Options".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def addList(self, listData):

        ##########################################
        # listData = dictionary
        ##########################################
        self.headers = {"Content-Type": "application/json"}
        url = "{0}/AddList".format(self.baseURL)
        rData = self.__genericPutRequest__(url, listData)
        self.headers = None
        return rData

    def deleteList(self, listId):
        
        ##########################################
        # listId = string
        ##########################################

        url = "{0}/DeleteList".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def deleteLists(self, listIds):

        ##########################################
        # listIds = list
        ##########################################

        self.headers = {"Content-Type": "application/json"}
        url = "{0}/DeleteLists".format(self.baseURL)
        rData = self.__genericPutRequest__(url, listIds)
        self.headers = None
        return rData

    def deleteListHistory(self, listId):
        
        ##########################################
        # listId = string
        ##########################################

        url = "{0}/DeleteListHistory".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def disableList(self, listId):

        ##########################################
        # listId = string
        ##########################################
        url = "{0}/DisableList".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericPutRequest__(url, "")
        return rData

    def disableLists(self, listIds):

        ##########################################
        # listId = listIds
        ##########################################
        self.headers = {"Content-Type": "application/json"}
        url = "{0}/DisableLists".format(self.baseURL)
        rData = self.__genericPutRequest__(url, listIds)
        self.headers = None
        return rData

    def enableList(self, listId):

        ##########################################
        # listId = string
        ##########################################
        url = "{0}/EnableList".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericPutRequest__(url, "")
        return rData

    def enableLists(self, listIds):

        ##########################################
        # listId = listIds
        ##########################################
        self.headers = {"Content-Type": "application/json"}
        url = "{0}/EnableLists".format(self.baseURL)
        rData = self.__genericPutRequest__(url, listIds)
        self.headers = None
        return rData

    def list(self, listId):

        ##########################################
        # listId = string
        ##########################################

        url = "{0}/List".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def lists(self, simple, threatListsOnly):

        ##########################################
        # simple = boolean
        # threatListsOnly = boolean
        ##########################################

        url = "{0}/Lists".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def listCount(self, listId, threatListsOnly):

        ##########################################
        # listId = string
        # threatListsOnly = boolean
        ##########################################

        url = "{0}/ListCount".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def stats(self, listId, threatListsOnly):

        ##########################################
        # listId = string
        # threatListsOnly = boolean
        ##########################################

        url = "{0}/Stats".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def updateList(self, force, listId):

        ##########################################
        # force = boolean
        # listId = string
        ##########################################

        url = "{0}/UpdateList".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def updateLists(self, listIds):

        ##########################################
        # listIds = list
        ##########################################
        url = "{0}/UpdateLists".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, listIds)
        self.headers = None
        return rData

    def updateListContents(self, append, listId, files):

        ##########################################
        # append = boolean
        # listId = string
        # files = dictionary of files: {"filename": open("filename", "rb")}
        ##########################################

        url = "{0}/updatelistcontents/{1}?apiKey={2}".format(self.baseURL, listId, self.apiKey)
        try:
            r = requests.put(url, headers = self.headers, files = files, data = None, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = json.loads(r.content.decode("utf-8"))
            else:
                rData = json.loads(r.content)
            return rData
        except Exception as err:
            return {"success": False, "error": err}

    def updateListProperties(self, updatedFeed):

        ##########################################
        # updatedFeed = dictionary
        ##########################################
        url = "{0}/UpdateListProperties".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, updatedFeed)
        self.headers = None
        return rData

    def validateList(self, listData):

        ##########################################
        # updatedFeed = dictionary
        ##########################################
        url = "{0}/ValidateList".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, listData)
        self.headers = None
        return rData

    def viewListHistory(self, firstRecord, listId, maxResults):
        
        ##########################################
        # firstRecord = Int32
        # listId = string
        # maxResults = Int32
        ##########################################

        url = "{0}/ViewListHistory".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        
        rData = self.__genericGetRequest__(url)
        return rData

    def addRecord(self, recordData, listId):

        ##########################################
        # recordData = list
        # listId = string
        ##########################################

        url = "{0}/AddRecord?listid={1}".format(self.baseURL, listId)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, recordData)
        self.headers = None
        return rData

    def deleteListRecord(self, recordsIds, listId):
        
        ##########################################
        # recordsIds = list
        # listId = string
        ##########################################

        self.headers = {"Content-Type": "application/json"}
        url = "{0}/DeleteRecord?listId={1}".format(self.baseURL, listId)
        rData = self.__genericDeleteRequest__(url, recordsIds)
        self.headers = None
        return rData

    def deleteListRecords(self, listId):
        
        ##########################################
        # listId = string
        ##########################################
        url = "{0}/DeleteListRecords?listId={1}".format(self.baseURL, listId)
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def deleteRecordModification(self, itemId, listId):
        
        ##########################################
        # listId = string
        # itemId = string
        ##########################################

        url = "{0}/DeleteListRecords".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params":
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericDeleteRequest__(url, None)
        return rData

    def listRecords(self, ascending, firstRecord, itemId, listId, maxResults, orderBy, simple, threatListsOnly):

        ##########################################
        # ascending = boolean
        # firstRecord - Int32
        # itemId = string
        # listId = string
        # maxResults = Int32
        # orderBy = string
        # simple = boolean
        # threatListsOnly = boolean
        ##########################################

        url = "{0}/ListRecords".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params" and x is not None:
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def modifyRecord(self, recordData):

        ##########################################
        # recordData = dictionary
        ##########################################

        url = "{0}/ModifyRecord".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, recordData)
        self.headers = None
        return rData

    def viewRecordModifications(self, firstRecord, listId, maxResults):

        ##########################################
        # firstRecord - Int32
        # listId = string
        # maxResults = Int32
        ##########################################

        url = "{0}/ViewRecordModifications".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params" and x is not None:
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def search(self, address, ascending, email, hash, indexId, listId, mutex, orderBy):

        ##########################################
        # address = string
        # ascending - boolean
        # email = string
        # hash = string
        # indexId = string
        # listId = string
        # mutex = string
        # orderBy = string
        ##########################################

        url = "{0}/Search".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params" and x is not None:
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def batchSearch(self, searchData):

        ##########################################
        # searchData = dictionary
        ##########################################

        url = "{0}/BatchSearch".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, searchData)
        self.headers = None
        return rData

    def wildcardSearch(self, address, ascending, email, hash, indexId, listId, mutex, orderBy):

        ##########################################
        # address = string
        # ascending - boolean
        # email = string
        # hash = string
        # indexId = string
        # listId = string
        # mutex = string
        # orderBy = string
        ##########################################

        url = "{0}/WildcardSearch".format(self.baseURL)
        params = []
        for x in locals():
            if x is not "self" and x is not "url" and x is not "params" and x is not None:
                params.append(x)
        for x in params:
            if locals()[x]:
                if "?" in url:
                    url += "&{0}={1}".format(x, locals()[x])
                else:
                    url += "?{0}={1}".format(x, locals()[x])
        rData = self.__genericGetRequest__(url)
        return rData

    def feedParsers(self):

        url = "{0}/FeedParsers".format(self.baseURL)
        rData = self.__genericGetRequest__(url)
        return rData

    def testFeedParser(self, feedData):

        ##########################################
        # recordData = dictionary
        ##########################################

        url = "{0}/TestFeedParser".format(self.baseURL)
        self.headers = {"Content-Type": "application/json"}
        rData = self.__genericPutRequest__(url, feedData)
        self.headers = None
        return rData

class fidelisNetwork():

    def __init__(self, ip, username, password, useuid, ignoressl):
        self.baseURL = "https://{0}/query".format(ip)
        self.username = username
        self.password = password
        self.headers = None
        self.ignoressl = ignoressl
        if self.ignoressl:
            self.checkURL = False
        else:
            self.checkURL = True
        if useuid:
            self.uid = self.getAuthToken(username, password)
        else:
            self.uid = None
        self.lastError = ""

    def getAuthToken(self, username, password):
        
        #Create the authentication URL
        url = "{0}/login.cgi?user={1}&pass={2}".format(self.baseURL, username, password)

        #Ignore SSL errors if specified
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        try:
            r = requests.get(url, verify=self.checkURL)
            if type(r.content) == bytes:
                rData = r.content.decode("utf-8")
            else:
                rData = r.content
        except Exception as err:
            self.lastError = "Error performing get request to URL- {0}".format(err)
            return None
        try:
            columns = rData.split("\n")[0].split("\t")
            entries = rData.split("\n")[1:-1]
            data = []
            for entry in entries:
                predata = entry.split("\t")
                item = {}
                for x in range(0, len(columns)):
                    item[columns[x]] = predata[x]
                data.append(item)
            jsonReturn = {"success": True, "error": None, "data": data}
            return jsonReturn["data"][0]["uid"]
        except Exception as err:
            self.lastError = err
            return None

    def execute(self, query, inputData):

        ##############################################################################################
        # query = string (the cgi name to perform, for example aac_alerts)
        # inputData = dictionary (parameter and value pairs to pass into the query
        #
        # =========
        # EXAMPLE:
        # =========
        #
        # query = "aac_alerts"
        #
        # inputData = {"alert_id": "29482"}
        # 
        # 
        # the data returned is always in JSON format and has the following structure:
        # 
        # {"success": <True|False>, "error": <error-msg-if-any>, "data": <data-returned-by-call>}
        # 
        ##############################################################################################

        if self.uid is not None:
            url = "{0}/{1}.cgi?uid={2}".format(self.baseURL, query, self.uid)
        else:
            url = "{0}/{1}.cgi?user={2}&pass={3}".format(self.baseURL, query, self.username, self.password)

        #Populate the input_parameters on the URL
        if inputData is not None:
            for k in inputData:
                url+= "&{0}={1}".format(k, inputData[k])

        #Ignore SSL errors if specified
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()

        try:
            #Perform the get request
            r = requests.get(url, verify=self.checkURL)
            
            #Decode from utf-8 if encoded
            if type(r.content) == bytes:
                rData = r.content.decode("utf-8")
            else:
                rData = r.content

            #Remove HTML encoding
            rData = unquote(rData)
        except Exception as err:
            self.lastError = "Error performing get request to URL- {0}".format(err)
            return err
        try:
            columns = rData.split("\n")[0].split("\t")
            entries = rData.split("\n")[1:-1]
            data = []
            for entry in entries:
                predata = entry.split("\t")
                item = {}
                for x in range(0, len(columns)):
                    item[columns[x]] = predata[x]
                data.append(item)
            jsonReturn = {"success": True, "error": None, "data": data}
            return jsonReturn
        except Exception as err:
            return err
        
