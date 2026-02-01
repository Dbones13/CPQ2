from CPQ_SF_SC_Modules import CL_SC_Modules

def getSiteNumber(Quote, Product, TagParserQuote, Session):
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
    Selected_MSID = []
    MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
    resDict = dict()
    for row in MSID_Cont.Rows:
        if row.IsSelected == True:
            Selected_MSID.append(row['MSIDs'])

    if Selected_MSID:
        SummaryTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, Selected_MSID, isParent)
        for models in SummaryTable.records:
            msid_name  = str(models.Parent['Name'])
            systemNumber = str(models.SiteLicSeqSys__c).strip()
            if msid_name not in resDict.keys() and systemNumber.isnumeric():
                resDict[msid_name] = systemNumber
            if len(resDict) == len(Selected_MSID):
                break
    return resDict