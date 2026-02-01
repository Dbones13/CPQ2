import datetime
def getAuthToken(Session=dict()):
    if "ISessionProxy" in str(type(Session)):
        if Session["token_generator"]:
            token_dict = Session["token_generator"]
            token_expire_time = token_dict.keys()[0]
            # Log.Write('Entered Condition 1')
            Trace.Write(token_expire_time > datetime.datetime.today() + datetime.timedelta(0,10))
            if token_expire_time > datetime.datetime.today() + datetime.timedelta(0,10):
                return "{}".format(token_dict[token_expire_time])
            else:
                # Log.Write('Entered Condition 2')
                query="select Value from HPS_INTEGRATION_PARAMS where [Key] ='{}'".format("CPS_URL")
                response = SqlHelper.GetFirst(query)
                res = AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('CPS', response.Value+'/oauth/token')
                token_dict = {datetime.datetime.today() + datetime.timedelta(0,res.expires_in) : "{} {}".format(res.token_type , res.access_token)}
                Session["token_generator"] = token_dict
                return "{} {}".format(res.token_type , res.access_token)
        else:
            # Log.Write('Entered Condition 3')
            query="select Value from HPS_INTEGRATION_PARAMS where [Key] ='{}'".format("CPS_URL")
            response = SqlHelper.GetFirst(query)
            res = AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('CPS', response.Value+'/oauth/token')
            token_dict = {datetime.datetime.today() + datetime.timedelta(0,res.expires_in) : "{} {}".format(res.token_type , res.access_token)}
            Session["token_generator"] = token_dict
            return "{} {}".format(res.token_type , res.access_token)
    else:
        # Log.Write('Entered Condition 4')
        query="select Value from HPS_INTEGRATION_PARAMS where [Key] ='{}'".format("CPS_URL")
        response = SqlHelper.GetFirst(query)
        res = AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('CPS', response.Value+'/oauth/token')
        token_dict = {datetime.datetime.today() + datetime.timedelta(0,res.expires_in) : "{} {}".format(res.token_type , res.access_token)}
        Session["token_generator"] = token_dict
        return "{} {}".format(res.token_type , res.access_token)

def getPricesFromCPS(header , record):
    url = "https://cpservices-pricing.cfapps.us10.hana.ondemand.com"
    endPoint = "/api/v1/statelesspricing"
    #Log.Info("URL:"+str(url)+"EP:"+str(endPoint)+"reco:"+str(RestClient.SerializeToJson(record))+"head:"+str(header))
    res = RestClient.Post('{}{}'.format(url , endPoint) , RestClient.SerializeToJson(record), header)
    return res


def getPrice(Quote,priceDict,partNumberrList,TagParserQuote, Session=dict(),isBulkUpload=False):
    null = None
    true = True
    false = False
    cartItems = []
    currencyCode = Quote.SelectedMarket.CurrencyCode
    salesArea = Quote.GetCustomField("Sales Area").Content
    pricingType = "SY" if Quote.GetCustomField("Quote Type").Content in ('Projects') else  ''
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
    kunnr = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SoldToCustomerId) )*>")
    listdict = eval(Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content) if Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content else []

    #partNumberrList = ['PD-CFFCE-200','CC-ZC3002','SLG720','MZ-PCEH15']

    itemIdDict = dict()

    itemId = 0
    for part in partNumberrList:
        itemId += 1
        itemIdDict[str(itemId)] = part
        pricelistval = pricingType
        if part in listdict:
            if Quote.GetCustomField('Booking LOB').Content == 'PMC' and Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
                pricelistval = Quote.GetCustomField('Customer Price List').Content
            else:
                pricelistval = "SY"
        prodh1 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))) {<* TABLE ( SELECT SBU_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>} {[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))) {<* TABLE ( SELECT SBU_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh2 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT LOB_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT LOB_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh3 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_FAMILY_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_FAMILY_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh4 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_LINE_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_LINE_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh5 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_LINE_SUBGROUP_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_LINE_SUBGROUP_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
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
                            "{}".format(pricelistval)
                        ]
                    },
                     {
                    "name": "KOMK-KUNNR",
                    "values": [
                        str(kunnr)
                    ]
                    },
                    {
                        "name": "KOMP-ZZPRODH1",
                        "values": [
                            str(prodh1)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH2",
                        "values": [
                            str(prodh2)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH3",
                        "values": [
                            str(prodh3)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH4",
                        "values": [
                            str(prodh4)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH5",
                        "values": [
                            str(prodh5)
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
                "variantConditions": [],
                "statistical": true,
                "subItems": []
            })

    #Trace.Write(str(cartItems))
    body["items"] = cartItems
    Trace.Write(RestClient.SerializeToJson(body))
    bearerToken = getAuthToken(Session)
    Trace.Write("bearerToken = " + str(bearerToken))
    header = {'Authorization': bearerToken}
    res = getPricesFromCPS(header , body)
    Trace.Write(RestClient.SerializeToJson(res))
    #Trace.Write(str(itemIdDict))
    #Trace.Write(res.id)
    itemsList = res.items
    tariffPCTDict = {}
    for item in itemsList:
        conditionList = item["conditions"]
        if conditionList:
            for condition in conditionList:
                if str(condition["conditionType"]) in ('ZP00','ZQ00'):
                    priceDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
                if isBulkUpload and str(condition["conditionType"]) == 'ZTSC': #Tariff
                    tariffPCTDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
    Trace.Write(" ----CPS List Price ---------- "+str(priceDict))
    Trace.Write(" ----CPS List Price ---------- "+str(tariffPCTDict))
    if isBulkUpload:
        return priceDict, tariffPCTDict
    else:
        return priceDict

def getTariffPrice(Quote,priceDict,partNumberrList,TagParserQuote, Session=dict()):
    null = None
    true = True
    false = False
    cartItems = []
    currencyCode = Quote.SelectedMarket.CurrencyCode
    salesArea = Quote.GetCustomField("Sales Area").Content
    pricingType = "SY" if Quote.GetCustomField("Quote Type").Content in ('Projects') else  ''
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
    
    listdict = eval(Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content) if Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content else []

    #partNumberrList = ['PD-CFFCE-200','CC-ZC3002','SLG720','MZ-PCEH15']

    itemIdDict = dict()

    itemId = 0
    kunnr = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SoldToCustomerId) )*>")
    for part in partNumberrList:
        itemId += 1
        itemIdDict[str(itemId)] = part
        pricelistval = pricingType
        
        if part in listdict:
            if Quote.GetCustomField('Booking LOB').Content == 'PMC' and Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
                pricelistval = Quote.GetCustomField('Customer Price List').Content
            else:
                pricelistval = "SY"
        prodh1 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))) {<* TABLE ( SELECT SBU_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>} {[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))) {<* TABLE ( SELECT SBU_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh2 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT LOB_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT LOB_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh3 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_FAMILY_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_FAMILY_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh4 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_LINE_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_LINE_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
        prodh5 = TagParserQuote.ParseString("[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC),[IN](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot, Projects))){<* TABLE ( SELECT PRODUCT_LINE_SUBGROUP_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{[IF]([AND]([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>, LSS),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>, Parts and Spot))){<* TABLE ( SELECT PRODUCT_LINE_SUBGROUP_CODE FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '" + str(part) +"' ) *>}{}[ENDIF]}[ENDIF]")
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
                            "{}".format(pricelistval)
                        ]
                    },
                    {
                    "name": "KOMK-KUNNR",
                    "values": [
                        str(kunnr)
                    ]
                    },
                    {
                        "name": "KOMP-ZZPRODH1",
                        "values": [
                            str(prodh1)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH2",
                        "values": [
                            str(prodh2)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH3",
                        "values": [
                            str(prodh3)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH4",
                        "values": [
                            str(prodh4)
                        ]
                    },
                    {
                        "name": "KOMP-ZZPRODH5",
                        "values": [
                            str(prodh5)
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
                    "variantConditions": [],
                    "statistical": true,
                    "subItems": []
                })
    
    Trace.Write(str(cartItems))
    body["items"] = cartItems
    #Trace.Write(RestClient.SerializeToJson(body))
    bearerToken = getAuthToken(Session)
    # Trace.Write("bearerToken = " + str(bearerToken))
    header = {'Authorization': bearerToken}
    res = getPricesFromCPS(header , body)
    Trace.Write(RestClient.SerializeToJson(res))
    #Trace.Write(str(itemIdDict))
    #Trace.Write(res.id)
    itemsList = res.items
    tariffPCTDict = {}
    for item in itemsList:
        conditionList = item["conditions"]
        if conditionList:
            for condition in conditionList:
                if str(condition["conditionType"]) in ('ZP00','ZQ00'):
                    priceDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
                if str(condition["conditionType"]) == 'ZTSC':
                    tariffPCTDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
    # Trace.Write(" ----CPS List Price ---------- "+str(priceDict))
    Trace.Write(" ----CPS Tariff ---------- "+str(tariffPCTDict))
    return priceDict,tariffPCTDict

def getCYBERPrice(Quote,priceDict,part,TagParserQuote, Session=dict()):
    null = None
    true = True
    false = False
    cartItems = []
    currencyCode = Quote.SelectedMarket.CurrencyCode
    salesArea = Quote.GetCustomField("Sales Area").Content
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

    itemIdDict = dict()
    part_number_list = SqlHelper.GetList('SELECT Part_Number FROM CT_CYBER_PRICINGLISTTYPE')
    listdict = [i.Part_Number for i in part_number_list]


    itemId = 0
    itemId += 1
    itemIdDict[str(itemId)] = part
    if part in listdict:
        pricelistval = "SY"
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
                            "{}".format(pricelistval)
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
                "variantConditions": [],
                "statistical": true,
                "subItems": []
            })
    body["items"] = cartItems
    bearerToken = getAuthToken(Session)
    header = {'Authorization': bearerToken}
    Log.Info("body---->cps--->"+str(body))
    res = getPricesFromCPS(header , body)
    itemsList = res.items
    if itemsList:
        for item in itemsList:
            conditionList = item["conditions"]
            for condition in conditionList:
                if str(condition["conditionType"]) in ('ZP00','ZQ00'):
                    priceDict[itemIdDict[str(item["itemId"])]] = str(condition["conditionRate"])
    if priceDict:
        return priceDict[part]