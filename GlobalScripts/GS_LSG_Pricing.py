from GS_GetPriceFromCPS import getAuthToken, getPricesFromCPS
import GS_FME_CONFIG_MOD


def getPrice(Quote,priceDict,partNumberrList,TagParserQuote, assignpart,isTrace=False):
    null = None
    true = True
    false = False
    cartItems = []
    currencyCode = Quote.SelectedMarket.CurrencyCode
    salesArea = Quote.GetCustomField("Sales Area").Content
    pricingType = "SY" if Quote.GetCustomField('Quote Type').Content in ('Projects') else  ''
    effectiveDate = Quote.EffectiveDate.Date.ToString('yyyy-MM-dd')
    a_land = TagParserQuote.ParseString("[IF]([EQ](<* LIST ( SELECT COUNT (MARKET_CODE) FROM CT_SALESORG_MISSING_MARKET WHERE MARKET_CODE = '<*CTX( Market.Code )*>' ) *>,0)){}{<*CTX( Quote.CustomField(Sales Area) )*>}[ENDIF]")
    pricingProcedure = TagParserQuote.ParseString("[IF]([EQ](<* LIST ( SELECT COUNT (MARKET_CODE) FROM CT_SALESORG_MISSING_MARKET WHERE MARKET_CODE = '<*CTX( Market.Code )*>' ) *>,0)){ZCPS07}{ZCPS04}[ENDIF]")

    body = {
        "docCurrency": "USD",
        "locCurrency": null,
        "pricingProcedure": "{}".format(pricingProcedure),
        "groupCondition": false,
        "itemConditionsRequired": true,
    }

    #partNumberrList = ['PD-CFFCE-200','CC-ZC3002','SLG720','MZ-PCEH15']

    itemIdDict = dict()

    itemId = 0
    for part in partNumberrList:
        itemId += 1
        itemIdDict[str(itemId)] = part
        cartItems.append({
                "itemId": "{}".format(itemId),
                "externalId": null,
                "quantity": {
                    "value": "1",
                    "unit": "EA"
                },
                "exchRateType": "M",
                "exchRateDate": "{}".format(Quote.EffectiveDate.Date.ToString('yyyy-MM-dd')),
                "productDetails": {
                    "productId": "{}".format(part),
                    "baseUnit": "EA",
                    "alternateProductUnits": null
                },
                "attributes": [
                    {
                        "name": "KOMK-ALAND",
                        "values": [
                            "{}".format(a_land)
                        ]
                    },
                    {
                        "name": "KOMK-SPART",
                        "values": [
                            "10"
                        ]
                    },
                    {
                        "name": "KOMP-SPART",
                        "values": [
                            "10"
                        ]
                    },
                    {
                        "name": "KOMP-PMATN",
                        "values": [
                            "{}".format(part)
                        ]
                    },
                    {
                        "name": "KOMK-WAERK",
                        "values": [
                            "{}".format(currencyCode)
                        ]
                    },
                    {
                        "name": "KOMP-PRSFD",
                        "values": [
                            "X"
                        ]
                    },
                    {
                        "name": "KOMK-VKORG",
                        "values": [
                            "{}".format(salesArea)
                        ]
                    },
                    {
                        "name": "KOMK-VTWEG",
                        "values": [
                            "10"
                        ]
                    },
                    {
                        "name": "KOMK-PLTYP",
                        "values": [
                            "{}".format(pricingType)
                        ]
                    }
                ],
                "accessDateList": [
                    {
                        "name": "KOMK-PRSDT",
                        "value": "{}".format(effectiveDate)
                    },
                    {
                        "name": "KOMK-FBUDA",
                        "value": "{}".format(effectiveDate)
                    }
                ],
                "variantConditions": assignpart,
                "statistical": true,
                "subItems": []
            })

    #Trace.Write(str(cartItems))
    body["items"] = cartItems
    Trace.Write(RestClient.SerializeToJson(body))
    bearerToken = getAuthToken()
    Trace.Write("bearerToken = " + str(bearerToken))
    header = {'Authorization': bearerToken}
    res = getPricesFromCPS(header , body)
    Trace.Write(RestClient.SerializeToJson(res))
    #Trace.Write(str(itemIdDict))
    Trace.Write('CPS Response received...')
    if isTrace:
        Trace.Write('Trace Software Condition entered')
        return res
    itemsList = res.items
    for item in itemsList:
        conditionList = item["conditions"]
        #Trace.Write(str(conditionList))
        for condition in conditionList:
            if str(condition["conditionType"]) in ('ZP00','ZQ00'):
                priceDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
    Trace.Write(str(priceDict))
    return priceDict

def getValue(userInput):
    try:
        return int(userInput)
    except:
        return str(userInput)


def getAccessToken(host):
    url = "https://{}/v2/oauth/accesstoken".format(host)
    res = AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('SAP_FME2Config_APIGEE', str(url))
    return "{} {}".format(res.token_type , res.access_token)

def assignval(resp):
    Log.Info(str(resp))
    a_arr = []
    for atnm in list(resp):
        a_dict=dict()
        '''Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
        a = Product.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
        if a == "DropDown":
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
        elif a == "Free Input, no Matching":
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
        else:
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
            Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))'''
        a_dict["factor"] = getValue(atnm["atwtb"])
        a_dict["key"] = str(atnm["atnam"])
        a_arr.append(a_dict)
    return a_arr

def GetListPriceFromCPS(quote, partNumbers, ProductHelper, TagParserQuote, host):
    hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)").HostName
    accessTkn = getAccessToken(hostquery)
    #partNumbers = [{'AS-UTRACS-N-S-SS-SS-NN-AA-NN-03-00-03-01-00-01-01-00-01-00-00-00-NN-N-S-P-001-N':'AS-UTRACS'}]
    Trace.Write(RestClient.SerializeToJson(partNumbers))
    for partDicts in partNumbers:
        for partDict in partDicts:
            try:
                jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,partDicts[partDict],partDict)
                _product=ProductHelper.CreateProduct("AS-UTRACS")
                for atnm in list(jsonConfig):
                    for att in _product.Attributes:
                        if  str(atnm["atnam"]) in ["V_35YY2312_LEVEL_UPGRAD_FACTOR","V_35YY2312_PERIOD_FACTOR","V_35YY2312_PERIOD_QUANTITY"]:
                            continue
                        if att.SystemId == str(atnm["atnam"]):
                            dis = _product.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
                            if dis == "DropDown":
                                _product.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
                            elif dis == "FreeInputNoMatching":
                                _product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(int(atnm["atwtb"])))
                            else:
                                _product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
                            Trace.Write(att.SystemId)
                _product.ApplyRules()
                Trace.Write('Total Price Calculated')
                c=_product.TotalPrice
                return _product.TotalPrice
            except BaseException as e:
                traceback = sys.exc_info()[2]
                #   Product.ErrorMessages.Add('Please enter valid FME Code')
                Trace.Write("Error from CPS Pricing: Please enter valid FME Code")
                Log.Error("Error from CPS Pricing: Please enter valid FME Code"+str(e)+ ". Error in row: " + str(traceback.tb_lineno))
                jsonconfig=''
            return ""