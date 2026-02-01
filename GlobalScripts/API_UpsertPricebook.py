def getAuthToken():
    url = "https://honeywellinternational-tst.cpq.cloud.sap"
    endPoint = "/basic/api/token"

    query = "select * from HPS_Integration_Params"
    paramDict = dict()
    for res in SqlHelper.GetList(query):
        paramDict[res.Key] = res.Value

    authString = "grant_type=password&username={}&password={}&domain={}"
    authString = authString.format(paramDict["CPI_USERNAME"] , paramDict["CPI_PASSWORD"] , paramDict["Domain_Name"])

    res = RestClient.Post('{}{}'.format(url , endPoint) , authString)
    return "{} {}".format(res.token_type , res.access_token)

def deleteEntry(header , pricebookId , entry):
    url = "https://s21.webcomcpq.com"
    endPoint = "/api/v1/admin/Pricebooks/DeletePricebookEntry?pricebookId={}&entryId={}".format(pricebookId , entry)

    try:
        RestClient.Post('{}{}'.format(url , endPoint) , {} , header)
        res = {"status" : 200 , "message" : "Record deleted"}
    except:
        res = {"status" : 500 , "message" : "Error Occured"}
    return res

def updatePricebookEntry(header , record , pricebookId , id = 0):
    url = "https://s21.webcomcpq.com"
    endPoint = "/api/v1/admin/Pricebooks/SavePricebookEntry?pricebookId={}".format(pricebookId)
    record["Id"] = id
    #Log.Write('{}'.format(record))
    try:
        r = RestClient.Post('{}{}'.format(url , endPoint) , RestClient.SerializeToJson(record), header)
        #Log.Write(RestClient.SerializeToJson(r))
        res = {"status" : 200 , "message" : "Record Saved" if id else "Record Created"}
    except:
        res = {"status" : 500 , "message" : "Error Occured"}
    return res

def upsertPricebookEntry(pricebookCode , record):
    fromDate = UserPersonalizationHelper.CovertToDate(str(record["ValidFrom"]))

    pricebookId = SqlHelper.GetFirst("select Id from PriceBookTableDefn where Code = '{}'".format(pricebookCode))
    entry = SqlHelper.GetFirst("select cpqTableEntryId from {} where PriceDescription = '{}' and ValidFrom = {}".format(pricebookCode , bodyData["record"]["PriceDescription"] , fromDate.ToOADate() - 2))

    bearerToken = getAuthToken()
    header = {'Authorization': bearerToken}

    if str(bodyData["delete"]) == "false":
        if entry:
            res = updatePricebookEntry(header , record , pricebookId.Id , entry.cpqTableEntryId)
        else:
            res = updatePricebookEntry(header , record , pricebookId.Id)
    elif str(bodyData["delete"]) == "true" and entry:
        res = deleteEntry(header , pricebookId.Id , entry.cpqTableEntryId)
    else:
        res = {"status" : 500 , "message" : "No Action Taken"}
    return ApiResponseFactory.JsonResponse(res , res["status"])
bodyData = RestClient.DeserializeJson(RequestContext.Body)
#Log.Write(str(bodyData["record"]))
ApiResponse = upsertPricebookEntry(str(bodyData["pricebookCode"]).replace('.','') , bodyData["record"])
