from CPQ_SF_SC_Modules import CL_SC_Modules

errorList=[err for err in Product.Attr('Error_Message').GetValue().split(',') if err and not err.startswith('Error in Dynamic price calculation for Model: ')]
Product.Attr('Error_Message').AssignValue('')

quoteCurrency = Quote.SelectedMarket.CurrencyCode
query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
Exchange_Rate = float(query.Exchange_Rate)

# Dynamic Price calculation method
def GetDynamicPrice(partNumber, pQty):
    try:
        if not (pQty and partNumber):
            return 0
        prefixPart, sStr, pNum = partNumber.rpartition('-')
        pPrice = 0
        gQty = pQty
        if prefixPart:
            pData = SqlHelper.GetList("select PartNumber,Platform,BasePrice,Description, PriceType from SC_PRICING_SESP where PartNumber like '%{}%' and PartNumber<>'{}' and PriceDate <= GETDATE()".format(prefixPart,partNumber))
            pDict={}
            for trow in pData:
                rQty = trow.PartNumber[-1*len(pNum):]
                if not filter(lambda x: x.isdigit(), rQty.lower().replace('k','')):
                    continue
                if 'k' in rQty.lower():
                    rQty = int(filter(lambda x: x.isdigit(), rQty.lower().replace('k','')))*1000
                else:
                    rQty = int(filter(lambda x: x.isdigit(), rQty))
                pDict[rQty] = float(trow.BasePrice)
            minQty = min(pDict, key=pDict.get)
            kCnt=0
            while gQty>0 and kCnt<pQty:
                mQty = max(filter(lambda val: val <= gQty, pDict.keys()))
                if minQty == mQty:
                    pPrice = pPrice + pDict[mQty] * gQty/minQty
                    gQty = 0
                else:
                    pPrice += pDict[mQty]
                    gQty = gQty-mQty
                kCnt+=1
        pStatus = 'True'
        return pPrice/pQty, 'True'
    except:
        pStatus = 'Error in Dynamic price calculation for Model: ' + partNumber
    return 0, pStatus


class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountName = Quote.GetCustomField('Account Name').Content
AccountId = Quote.GetCustomField('AccountId').Content
#AccountSite = Quote.GetCustomField('Account Site').Content
pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
isParent = False
selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
AccountSite = selectedSites.split('<,>')
if not pAccountName:
    isParent = True
MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
SESP_Models_Cont = Product.GetContainerByName('SC_SESP Models')
SESP_Models_Cont.Clear()
SESP_Models_Hid_Cont = Product.GetContainerByName('SC_SESP Models Hidden')
SESP_Models_Hid_Cont.Clear()

Selected_MSID = []
Models_Summary = []
#MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
bundlePricingDict = {'sesp value plus':0.91, 'sesp value remote plus':1, 'value shield': 0.64}
for row in MSID_Cont.Rows:
    if row.IsSelected == True:
        Selected_MSID.append(row['MSIDs'])
if Selected_MSID:
    SummaryTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, Selected_MSID, isParent)
    for models in SummaryTable.records:
        msid_name  = models.Parent['Name']
        sys_name = models.Parent['ProductCode']
        i = SESP_Models_Cont.AddNewRow()
        hRow = SESP_Models_Hid_Cont.AddNewRow()
        hRow['MSID'] = i['MSID']  = msid_name.ToString()
        hRow['MSID_SFDC_ID'] = i['MSID_SFDC_ID']  = models.Parent['Id'].ToString()
        hRow['Model_SFDC_ID'] = i['Model_SFDC_ID']  = str(models.Id)
        hRow['Model#'] = i['Model#'] = str(models.ProductCode)
        hRow['System_Name'] = i['System_Name'] = sys_name.ToString()
        hRow['System_Number'] = i['System_Number'] = str(models.SiteLicSeqSys__c)
        hRow['Description'] = i['Description'] = str(models.Name)
        hRow['Qty'] = i['Qty'] = str(models.Quantity)
        hRow['UnitPrice'] = i['UnitPrice'] = '0'
        hRow['Price'] = i['Price'] = '0'
        Models_Summary.append(str(models.ProductCode))

# to load Model summary container from Models scope container:
mc = Product.GetContainerByName('SC_Models_Scope')
for i in mc.Rows:
    #if i.IsSelected == True:
    j = SESP_Models_Cont.AddNewRow()
    hRow = SESP_Models_Hid_Cont.AddNewRow()
    hRow['MSID'] = j['MSID'] = i['MSIDs']
    hRow['System_Name'] = j['System_Name'] = i['System_Name']
    hRow['System_Number'] = j['System_Number'] = i['System_Number']
    hRow['Platform'] = j['Platform'] = i['Platform']
    hRow['Model#'] = j['Model#'] = i['SESP_Models']
    hRow['Description'] = j['Description'] = i['Description']
    hRow['Qty'] = j['Qty'] = i['Quantity']
    hRow['UnitPrice'] = j['UnitPrice'] = '0'
    hRow['Price'] = j['Price'] = '0'
    Models_Summary.append(str(i['SESP_Models']))

if Models_Summary:
    cFactor = 1.1 if Product.Attr('SC_Coverage').GetValue().lower() == '24x7' else 1
    bFactor = bundlePricingDict[Product.Attr('SC_Service_Product').GetValue().lower()] if Product.Attr('SC_Service_Product').GetValue().lower()in bundlePricingDict else 1
    pData = SqlHelper.GetList("select PartNumber, Platform, BasePrice, Description, PriceType from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE()".format(str(tuple(Models_Summary)).replace(',)',')')))
    for val in pData:
        BasePrice = val.BasePrice
        for j in SESP_Models_Cont.Rows:
            if j['Model#'] == val.PartNumber:
                if val.PriceType == 'Dynamic':
                    BasePrice, pStatus = GetDynamicPrice(val.PartNumber, int(j['Qty']))
                    if pStatus != 'True':
                        errorList.append(pStatus)
                j['Platform'] = str(val.Platform)
                j['UnitPrice'] = str(round(((BasePrice *bFactor) * cFactor * Exchange_Rate),2))
                j['Price'] = str(round((((BasePrice *bFactor) * cFactor * Exchange_Rate)* int(j['Qty'])),2))
        for hRow in SESP_Models_Hid_Cont.Rows:
            if hRow['Model#'] == val.PartNumber:
                hRow['Platform'] = str(val.Platform)
                hRow['UnitPrice'] = str(round(((BasePrice *bFactor) * cFactor * Exchange_Rate),2))
                hRow['Price'] = str(round((((BasePrice *bFactor) * cFactor * Exchange_Rate)* int(hRow['Qty'])),2))
SESP_Models_Cont.Calculate()
SESP_Models_Hid_Cont.Calculate()
if errorList:
    Product.Attr('Error_Message').AssignValue(Product.Attr('Error_Message').GetValue() + ', ' + ', '.join(errorList) if Product.Attr('Error_Message').GetValue() else ', '.join(errorList))