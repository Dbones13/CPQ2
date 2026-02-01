def GetQuoteTableList():
    sqlQuery = "SELECT distinct(TABLE_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE 'QT__%'"
    sqlRes = SqlHelper.GetList(sqlQuery)
    resultArray = []
    for row in sqlRes:
        resultArray.append(row.TABLE_NAME)
    return resultArray

def GetQuoteInformation(sqlQuery):
    sqlRes = SqlHelper.GetList(sqlQuery)
    result = {}
    if sqlRes is not None:
        for row in sqlRes:
            result["DateCreated"]     = row.DATE_CREATED
            result["DateModified"]     = row.DATE_MODIFIED
            result["EffectiveDate"] = row.EFFECTIVE_DATE
    return result

def GetCartId(masterId, visitorId, revisionId):
    sqlQuery = "SELECT CART_ID FROM CART_REVISIONS WHERE MASTER_ID ={}  AND  VISITOR_ID = {} AND REVISION_ID = {}"
    sqlRes = SqlHelper.GetFirst(sqlQuery.format(masterId, visitorId, revisionId))
    result = {}
    if sqlRes is not None:
        result['cartId'] = sqlRes.CART_ID
    return result

res = {}
quoteTables = []
bodyData         = RestClient.DeserializeJson(RequestContext.Body)
quoteNumber     = str(bodyData["QuoteNumber"])
quoteOwnerId    = int(quoteNumber[: 4])
quoteMasterId     = int(quoteNumber[4:])
ownerId         = int(bodyData["OwnerId"])
quoteId         = int(bodyData["QuoteId"])
revisionId        = int(bodyData["Revision"])
#Log.Info("Test===>"+str(bodyData))
quoteInfo = {'CompositeNumber':quoteNumber, "Revision" : revisionId, 'OwnerId': ownerId, 'QuoteId': quoteId}
isValidInput = True

if len(quoteNumber) < 8:
    quoteInfo["CompositeNumber"] = "Invalid Quote Number"
    isValidInput = False

quoteResult = {}
if isValidInput:
    '''Get Quote Information'''
    sqlQuery = "SELECT CONVERT(VARCHAR(20),DATE_CREATED , 20) AS DATE_CREATED, CONVERT(VARCHAR(20),DATE_MODIFIED , 20) AS DATE_MODIFIED, CONVERT(VARCHAR(20),EFFECTIVE_DATE , 20) AS EFFECTIVE_DATE FROM cart WHERE cart_id = {} and userid = {}"
    quoteResult = GetQuoteInformation(sqlQuery.format(quoteMasterId, quoteOwnerId))
    if len(quoteResult) == 0:
        quoteInfo["CompositeNumber"] = "Quote Number does not exist"
        isValidInput = False

if isValidInput and quoteMasterId != quoteId:
    quoteInfo["QuoteId"] = "Invalid Quote Id"
    isValidInput = False

if isValidInput and quoteOwnerId != ownerId:
    quoteInfo["OwnerId"] = "Invalid Owner Id"
    isValidInput = False

if isValidInput:
    revisionResult = GetCartId(quoteId, ownerId, revisionId)
    if len(revisionResult) < 1:
        quoteInfo["QuoteId"] = "Invalid Revision Id"
        isValidInput = False
    else:
        quoteCartId = revisionResult['cartId']

if isValidInput:
    for key in quoteResult.keys():
        quoteInfo[key]    = quoteResult[key]
    '''Get Quote Table List'''
    quoteTableList = GetQuoteTableList()
    for quoteTableName in quoteTableList:
        quoteTableInfo = {"Rows": [], "QuoteTableName": ''}
        sqlQuery = "SELECT * FROM {} WHERE cartid = {} AND ownerId = {}".format(quoteTableName, quoteCartId, quoteOwnerId)
        sqlRes = SqlHelper.GetList(sqlQuery)
        for row in sqlRes:
            rowData = {}
            for column in row:
                rowData[column.Key] = column.Value
            quoteTableInfo["Rows"].append({"Row":rowData})
        quoteTableInfo["QuoteTableName"] = quoteTableName
        quoteTables.append(quoteTableInfo)
    quoteInfo["QuoteTables"] = quoteTables

res["Quote"] = quoteInfo
ApiResponse = ApiResponseFactory.JsonResponse(res)