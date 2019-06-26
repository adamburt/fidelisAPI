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
        url = url = "{0}/authenticate".format(self.baseURL)
        if method.lower() == "get":
            url += "?username={0}&password={1}".format(quote(username), quote(password))
            useGet = True
        
        #Ignore SSL errors if specified
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        if useGet:
            try:
                print(url)
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

    def __genericDeleteRequest__(self, url):
        if self.ignoressl:
            requests.packages.urllib3.disable_warnings()
        headers = self.headers
        try:
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
        rData = self.__genericDeleteRequest__(url)
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
        rData = self.__genericDeleteRequest__(url)
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
